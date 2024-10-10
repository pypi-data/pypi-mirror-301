import re
# import matplotlib.pyplot as plt
import polars as pl
import pandas as pd
import numpy as np
import boto3
from dataclasses import dataclass, field

# Turn off annoying pandas warnings
pd.options.mode.chained_assignment = None
pd.set_option("future.no_silent_downcasting", True)

def get_batches(pg_path):
    if pg_path.endswith(".csv"):
        sep = ","
    else:
        sep = "\t"
    lazy_df = pl.scan_csv(pg_path,
                        separator=sep,
                        # storage_options=self.get_storage_options(),
                        infer_schema_length=10000,
                        )
    column_names = lazy_df.collect_schema().names()
    batches = []
    for column in column_names:
        batch = re.search(r'SET\d+(-\d+)?REP\d+(-\d+)?', column)
        if isinstance(batch, re.Match):
            batches.append(batch[0])
    batches = list(set(batches))
    return batches

def get_proteins(pg_path):
    if pg_path.endswith(".csv"):
        sep = ","
    else:
        sep = "\t"
    df = pd.read_csv(pg_path, sep=sep)

    # Simplify protein ids. eg. P52701;P52701-2;P52701-3  -> P52701
    def process_protein_id(protein_id):
        id = protein_id.split(";")[0]
        return id.split("-")[0]

    df["Protein.Ids"] = df["Protein.Ids"].apply(process_protein_id)
    protein_id = df["Protein.Ids"]
    return list(set(protein_id.to_list()))

@dataclass
class DataLoader:

    def load_data(self, path, target=None):
        lazy_df = self._load_lazy_df(path)
        if target is not None:
            lazy_df = lazy_df.filter(pl.col("Genes").str.contains(target))#.collect(streaming=True).to_pandas()
    
        if "pg_matrix" in path:
            identifier_columns = ["Protein.Ids", "Genes"]
        else:
            identifier_columns = ["Protein.Ids", "Genes", "Precursor.Id"]
    
        # Collect all column names for filtering
        all_columns = lazy_df.collect_schema().names()
        column_names = identifier_columns + [col for col in all_columns if col.endswith(".d") and col not in bad_batches]
        
        # Collect the df
        if column_names is not None: 
            pep_df = lazy_df.select(column_names).collect(streaming=True).to_pandas()
        else: # Load in the whole thing!
            pep_df = lazy_df.collect(streaming=True).to_pandas()
    
        # Group by gene
        df = pep_df.sort_index(axis=1, level="Genes")
    
        return df

    def _detect_file_format(self, path):
        if path.endswith(".csv"):
            return "csv"
        elif path.endswith(".tsv"):
            return "tsv"
        else:
            raise ValueError(f"Unsupported file format for file: {path}")

    def _load_lazy_df(self, path):
        file_format = self._detect_file_format(path)
        sep = "," if file_format == "csv" else "\t"
        lazy_df = pl.scan_csv(path,
                        separator=sep,
                        storage_options=self.get_storage_options(),
                        infer_schema_length=10000,
                        )
        
        return lazy_df

    def get_storage_options(self) -> dict[str, str]:
        """Get AWS credentials to enable polars scan_parquet functionality.

        It's kind of annoying that this is currently necessary, but here we are...
        """
        credentials = boto3.Session().get_credentials()
        return {
            "aws_access_key_id": credentials.access_key,
            "aws_secret_access_key": credentials.secret_key,
            "session_token": credentials.token,
            "aws_region": "us-west-2",
        }

@dataclass
class ProcessUtils:

    label_screens: bool = True
    screen_split: dict = field(default_factory=lambda: {(0, 5863): "THP-1 1K",  # MSR numbers by which to split screens
                                                        (5863, 1e16): "Anborn"})

    def __post_init__(self):
        if self.label_screens:
            if self.screen_split is None:
                raise ValueError("A dictionary must be provided to label screens")
            missing_ranges = self._check_missing_ranges()
            if len(missing_ranges) > 0:
                raise ValueError(f"Missing MSR numbers in screen dictionary.\nUnable to label MSR numbers in range(s) {missing_ranges}.")


    def _split_batch_screen(self, df):
        df[['batch', 'screen']] = df['batch'].str.split('_', expand=True)
        return df
        
    
    def _get_batch_compound_names(self, pivot_df):
        pivot_df["batch"] = pivot_df["Compound"].astype(str).str.extract(r'(SET\d+(-\d+)?REP\d+(-\d+)?)')[0].astype("category").to_list()
        if self.label_screens:
            pivot_df["batch"] = pivot_df["batch"] + "_" + pivot_df["Compound"].apply(self._get_screen)
        pivot_df["Compound"] = pivot_df["Compound"].apply(self._get_compound_name)
        return pivot_df
    
    def _get_compound_name(self, s: str) -> str:
        """
        Extracts the compound name from the name of the file.
    
        Parameters
        ----------
        s: str
            An entry from the "Filename" column, a path to where the file is located
        
        Returns
        -------
        str
            The name of the treatment compound
        """
        # Look for compounds with the name TAL####
        if "TAL" in s.upper():
            tal_num = re.search(r'TAL\d+(-\d+)?', s)[0]
            # Strip leading zeros if present
            num = int(re.search(r'\d+(-\d+)?', tal_num)[0])
            new_name = "TAL" + str(num)
            return new_name
        elif "DMSO" in s.upper():
            return "DMSO"
        elif "PRTC" in s.upper():
            return "PRTC"
        elif "nuclei" in s.lower():
            return "NUC"
        elif "nuc" in s.lower(): # cases where it is labeled as NUC2
            nuc_num = re.search(r'NUC\d+(-\d+)?', s)
            if nuc_num is None:
                return "NUC"
            else:
                return nuc_num[0]
        elif "dbet" in s.lower():
            return "dBET6"
        elif "FRA" in s.upper():
            return "FRA"
        elif "none" in s.lower():
            return "None"
        else:
            raise Exception(f"Unable to extract compound name from filename {s}.")
    
    def _get_screen(self, msr_str):
        try:        
            msr = re.search(r'MSR\d+(-\d+)?', msr_str)[0]
        except:
            raise ValueError(f"Unable to match MSR for filename {msr_str}.")
        
        msr = int(re.search(r'\d+(-\d+)?', msr)[0])
    
        for msr_range, screen_name in self.screen_split.items():
            if msr_range[0] <= msr < msr_range[1]:
                return screen_name
        raise ValueError(f"Unable to determine screen for msr num {msr}.")
    
    def _check_missing_ranges(self):
        sorted_ranges = sorted(self.screen_split.keys())
        missing_ranges = []

        for i in range(len(sorted_ranges) - 1):
            current_end = sorted_ranges[i][1]
            next_start = sorted_ranges[i+1][0]

            if current_end < next_start:
                missing_ranges.append((current_end, next_start))
        return missing_ranges

@dataclass
class PeptideProcessor(ProcessUtils):

    label_screens: bool = True             # Should be true if more than one cell type in data
    screen_split: dict = field(default_factory=lambda: {(0, 5863): "THP-1 1K",  # MSR numbers by which to split screens
                                                        (5863, 1e16): "Anborn"})
    __pep_df: pd.DataFrame = None

    def process_and_normalize(self, pep_df):
        if "Precursor.Id" not in pep_df.columns:
            raise Exception("Precursor.Id not in dataframe columns")

        self.__pep_df = pep_df
        
        pivot_df = self._melt_pivot_df()
        pivot_df = self._get_batch_compound_names(pivot_df)
        normalized_df = self._median_normalize(pivot_df)
        if self.label_screens:
            normalized_df = self._split_batch_screen(normalized_df)

        self.__pep_df = None
        return normalized_df
    
    def _melt_pivot_df(self):
        quant_cols = quant_cols =  [col for col in self.__pep_df.columns if col.endswith(".d")]

        # Log transform 
        quant_pep_df = self.__pep_df.replace({None: np.nan,
                                             0: np.nan}).infer_objects(copy=False)
        quant_pep_df[quant_cols] = np.log(quant_pep_df[quant_cols].astype(float))

        # Restructure df so columns are peptides
        id_vars=["Protein.Ids", "Genes", "Precursor.Id"]    
        melt_df = quant_pep_df.melt(id_vars=id_vars, var_name="Compound", value_name="Log Abundance")
        pivoted_df = melt_df.pivot(index="Compound", columns=id_vars, values="Log Abundance")
        pivoted_df.reset_index(inplace=True) # Make compound a normal column
        return pivoted_df

    def _median_normalize(self, pivot_df):
    
        def subtract_median(group):
            return group - group.median().median()
            
        pivot_df.index = pivot_df["Compound"] # Temporarily make compound the index
        pivot_df.drop(columns=["Compound"], level=0, inplace=True)
        normalized_df = pivot_df.groupby(("batch", "", ""), observed=False).apply(subtract_median, include_groups=True)
        normalized_df.reset_index(inplace=True) # Remove batch from index
        return normalized_df

@dataclass
class ProteinProcessor(ProcessUtils):
    label_screens: bool = True             # Should be true if more than one cell type in data
    screen_split: dict = field(default_factory=lambda: {(0, 5863): "THP-1 1K",  # MSR numbers by which to split screens
                                                        (5863, 1e16): "Anborn"})
    dropna_threshold: float = 0.5

    __prot_df: pd.DataFrame = None


    def process_and_normalize(self, prot_df):
        if "Precursor.Id" in prot_df.columns:
            raise Exception("This is a pr_matrix file. Use PeptideProcessor class instead.")
        self.__prot_df = prot_df
        melt_df = self._melt_df()
        melt_df = self._get_batch_compound_names(melt_df)
        normalized = self._median_normalize(melt_df)
        if self.label_screens:
            normalized = self._split_batch_screen(normalized)
        self.__prot_df = None
        return normalized

    def _melt_df(self):

        quant_cols = [col for col in self.__prot_df.columns if col.endswith(".d")]

        # Log transform 
        quant_pep_df = self.__prot_df.replace({None: np.nan,
                                             0: np.nan}).infer_objects(copy=False)
        quant_pep_df[quant_cols] = np.log(quant_pep_df[quant_cols].astype(float))

        df = quant_pep_df[["Protein.Ids", "Genes"] + quant_cols]
        df = df.dropna(thresh=df.shape[0]*self.dropna_threshold)
        if df.empty:
            raise Exception("Dataframe is empty after dropping NaNs. Try lowering drpna_threshold.")
        melt_df = df.melt(id_vars=["Protein.Ids", "Genes"], var_name="Compound", value_name="Abundance")
        melt_df = melt_df.loc[melt_df["Abundance"].notna()]
        return melt_df

    def _median_normalize(self, melt_df):
        def subtract_median(group):
            # For a protein in a batch, eg. UBA1 in SET1REP1, subtractract the median abundance
            group["Abundance"] = group["Abundance"] - group["Abundance"].median()
            return group
        normalized_df = melt_df.groupby(["Genes", "batch"]).apply(subtract_median, include_groups=False).reset_index()
        dropcol = [col for col in normalized_df.columns if col.startswith("level")][0]
        normalized_df = normalized_df.drop(columns=dropcol)
        return normalized_df
        
@dataclass
class ProteinZScoreCalculator:

    def _compute_z_score(self, subdf):
        # Get the median abundance for the current screen
        med = subdf["Abundance"].median()

        # Get median absolute deviation
        subdf["abs dev"] = abs(subdf["Abundance"] - med)
        MAD = subdf["abs dev"].median()
        subdf.drop(columns=["abs dev"], inplace=True)

        # Calculate Z Score
        subdf["Z Score"] = (subdf["Abundance"] - med) / MAD
        return subdf

    def _get_median_z_score(self, z_scores):
        if "screen" in z_scores.columns.to_list():
            groups = ["screen", "Genes", "Compound"]
        else:
             groups = ["Genes", "Compound"]
        z_scores["med Z Score"] = z_scores.groupby(groups)["Z Score"].transform('median')
        return z_scores

    def compute_z_score(self, data):
        if "Precursor.Id" in data.columns.names:
            raise Exception("Precursor.Id in columns. Be sure to use pg_matrix with this class")
        
        if "screen" in data.columns.to_list():
            groups = ["screen", "Genes"]
        else:
             groups = ["Genes"]
        z_scores = data.groupby(groups).apply(self._compute_z_score, include_groups=False).reset_index()
        z_scores = self._get_median_z_score(z_scores)

        dropcol = [col for col in z_scores if col.startswith("level")]
        z_scores = z_scores.drop(columns=dropcol)
        return z_scores

@dataclass
class PeptideZScoreCalculator:

    def _compute_z_score(self, subdf):
        # Get median abundance for all peptides in the protein
        quant_cols = [col for col in subdf.columns if col not in [('batch', '', ''), ('Compound', '', ''),('screen', '', '')]]
        for column in quant_cols:
            MAD = abs(subdf[column] - subdf[column].median()).median()
            subdf[column] = (subdf[column] - subdf[column].median())/MAD
        return subdf

    def get_median_z_score(self, z_scores):
        if ("screen", "", "") in z_scores.columns.to_list():
            groups = [("screen", "", ""), ("Compound", "","")]
        else:
            groups = [("Compound", "","")]
        
        quant_cols = [col for col in z_scores.columns if col not in [('batch', '', ''), ('Compound', '', ''),('screen', '', '')]]
        return z_scores.groupby(groups)[quant_cols].median().reset_index()

    def compute_z_score(self, data):

        if "Precursor.Id" not in data.columns.names:
            raise Exception("Precursor.Id not in columns. Be sure to use pr_matrix with this class")
            
        if ("screen", "", "") in data.columns.to_list():
            groups = [("screen", "", "")]
            z_scores = data.groupby(groups).apply(self._compute_z_score, include_groups=False).reset_index()
        else:
            z_scores = self._compute_z_score(data)

        dropcol = [col for col in z_scores.columns if col[0].startswith("level")]
        z_scores = z_scores.drop(columns=dropcol)
        return z_scores

    def melt_z_score_df(self, z_scores):
        if ("screen", "", "") in z_scores.columns.to_list():
            id_cols = ['screen__', 'batch__', 'Compound__']
        else:
            id_cols = ['batch__', 'Compound__']

        z_scores_copy = z_scores.copy()
        z_reset = z_scores_copy.reset_index()
        z_scores_copy.columns = ['_'.join([str(i) for i in col]).strip() for col in z_scores_copy.columns] # Combine mulitindex columns
        df_melted = pd.melt(
            z_scores_copy, 
            id_vars=id_cols,
            value_vars=[col for col in z_scores_copy.columns if col not in id_cols],
            var_name='multiindex', 
            value_name='Abundance'
        )
        df_melted[['Protein.Ids', 'Genes', 'Precursor.Id']] = df_melted['multiindex'].str.split('_', expand=True) # Separate columns again
        df_melted = df_melted.drop(columns=['multiindex'])
        df_melted = df_melted.rename(columns={key: key.rstrip("_") for key in id_cols})
        return df_melted

high_abundance_batches = """MSR8360_SET11REP2A2_FRA12000_DIA.d
MSR8363_SET11REP2A5_TAL0001080_DIA.d
MSR8368_SET11REP2A10_TAL0000561_DIA.d
MSR8371_SET11REP2B1_TAL0000576_DIA.d
MSR8373_SET11REP2B3_TAL0000803_DIA.d
MSR8376_SET11REP2B6_DMSO_DIA.d
MSR8378_SET11REP2B8_TAL0000087_DIA.d
MSR8380_SET11REP2B10_TAL0000610_DIA.d
MSR8385_SET11REP2C3_TAL0000981_DIA.d
MSR8386_SET11REP2C4_TAL0000252_DIA.d
MSR8387_SET11REP2C5_TAL0000900_DIA.d
MSR8388_SET11REP2C6_TAL0000204_DIA.d
MSR8392_SET11REP2C10_TAL0001052_DIA.d
MSR8395_SET11REP2D1_TAL0000853_DIA.d
MSR8398_SET11REP2D4_TAL0001701_DIA.d
MSR8403_SET11REP2D9_TAL0000400_DIA.d
MSR8405_SET11REP2D11_TAL0001701_DIA.d
MSR8410_SET11REP2E4_TAL0000490_DIA.d
MSR8412_SET11REP2E6_TAL0000729_DIA.d
MSR8413_SET11REP2E7_TAL0000896_DIA.d
MSR8417_SET11REP2E11_TAL0000305_DIA.d
MSR8421_SET11REP2F3_TAL0000387_DIA.d
MSR8422_SET11REP2F4_TAL0000240_DIA.d
MSR8423_SET11REP2F5_TAL0000693_DIA.d
MSR8425_SET11REP2F7_TAL0000294_DIA.d
MSR8426_SET11REP2F8_TAL0000764_DIA.d
MSR8428_SET11REP2F10_TAL0001058_DIA.d
MSR8429_SET11REP2F11_TAL0000397_DIA.d
MSR8437_SET11REP2G7_TAL0000989_DIA.d
MSR8439_SET11REP2G9_TAL0001073_DIA.d
MSR8448_SET11REP2H6_TAL0000442_DIA.d
MSR8449_SET11REP2H7_TAL0000342_DIA.d
MSR8450_SET11REP2H8_TAL0000105_DIA.d
MSR8451_SET11REP2H9_TAL0000398_DIA.d
MSR8453_SET11REP2H11_TAL0000752_DIA.d
MSR9222_SET4REP3H12_TAL0000309_DIA.d
MSR9306_SET11REP3G12_TAL0000817_DIA.d
MSR9318_SET11REP3H12_TAL0001052_DIA.d"""

bad_batches = high_abundance_batches.split("\n")