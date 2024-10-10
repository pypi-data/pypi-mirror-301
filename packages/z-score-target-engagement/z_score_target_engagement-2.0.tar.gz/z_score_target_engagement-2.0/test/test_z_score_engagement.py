import unittest
import os
from z_score_engagement import *
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

class TestDataLoader(unittest.TestCase):

    test_pg_path = os.path.join(os.getcwd(), "test", "test_pg_matrix.csv")
    test_pr_path = os.path.join(os.getcwd(), "test", "test_pr_matrix.csv")

    def setUp(self):
        self.dl = DataLoader()

    def test_detect_file_format(self):
        self.assertEqual(self.dl._detect_file_format(self.test_pg_path), "csv")
        self.assertEqual(self.dl._detect_file_format("take_test_path.tsv"), "tsv")
        with self.assertRaises(ValueError):
            self.dl._detect_file_format("bad_path.xyz")
    
    def test_load_lazy_df(self):
        df = self.dl._load_lazy_df(self.test_pg_path)
        self.assertIsInstance(df, pl.lazyframe.frame.LazyFrame)
    
    def test_load_data(self):
        df = self.dl.load_data(self.test_pg_path)
        self.assertIsInstance(df, pd.core.frame.DataFrame)
        self.assertEqual(df.shape, (100, 578))
        df = self.dl.load_data(self.test_pr_path)
        self.assertIsInstance(df, pd.core.frame.DataFrame)
        self.assertEqual(df.shape, (10, 579))

class TestProcessUtils(unittest.TestCase):

    def setUp(self):
        self.p = ProcessUtils()

    def test_split_batch_screen(self):
        data = {
                'batch': ['SET1REP1_screen1', 'SET2REP2_screen2', 'SET3REP3_screen3'],
                'some_other_column': [1, 2, 3]
                }
        df = pd.DataFrame(data)
        result = self.p._split_batch_screen(df)
        expected_df = pd.DataFrame({
                                    'batch': ['SET1REP1', 'SET2REP2', 'SET3REP3'],
                                    'some_other_column': [1, 2, 3],
                                    'screen': ['screen1', 'screen2', 'screen3'],
                                    })
        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)
        pd.testing.assert_frame_equal(result, expected_df)

    def test_get_screen(self):
        self.assertEqual(self.p._get_screen('MSR5863_SET10REP2C3_TAL123_DIA.d'), "Anborn")
        self.assertEqual(self.p._get_screen('MSR8000_SET10REP2C3_TAL123_DIA.d'), "Anborn")
        self.assertEqual(self.p._get_screen('MSR12_SET10REP2C3_TAL123_DIA.d'), "THP-1 1K")
        with self.assertRaises(ValueError):
            self.p._get_screen('NOTASCREEN_SET10REP2C3_TAL123_DIA.d')

        # Test with new screen dict
        custom_screen_split = {(0, 100): "Screen A",  
                                (100, 1e16): "Screen B"}
        p = ProcessUtils(screen_split=custom_screen_split)
        self.assertEqual(p.screen_split, custom_screen_split)
        self.assertEqual(p._get_screen('MSR100_SET10REP2C3_TAL123_DIA.d'), "Screen B")
        self.assertEqual(p._get_screen('MSR50_SET10REP2C3_TAL123_DIA.d'), "Screen A")
        self.assertEqual(p._get_screen('MSR102_SET10REP2C3_TAL123_DIA.d'), "Screen B")
        
        # Test with missing MSR values
        with self.assertRaises(ValueError):
            p = ProcessUtils(screen_split={(0, 99): "Screen A",  # MSR numbers by which to split screens
                                       (100, 1e16): "Screen B"})

        
    def test_get_compound_name(self):
        compounds = ['MSR5863_SET10REP2C3_TAL123_DIA.d',
                     'MSR12_SET9REP14C3_TAL0000981_DIA.d',
                     'MSR10000_SET12REP3C3_TAL1052_DIA.d',
                     'MSR275_SET14REP15C3_FRA00012_DIA.d',
                     'MSR5864_SET14REP15C3_DMSO_DIA.d',
                     'MSR123_SET14REP15C3_NUC1_DIA.d',
                     'MSR5864_SET14REP15C3_NUC_DIA.d',
                     'MSR583_SET14REP15C3_DBET6_DIA.d',
                     'MSR674_SET14REP15C3_NONE_DIA.d']
        expected = ["TAL123",
                    "TAL981",
                    "TAL1052",
                    "FRA",
                    "DMSO",
                    "NUC1",
                    "NUC",
                    "dBET6",
                    "None"]
        result = [self.p._get_compound_name(s) for s in compounds]
        self.assertEqual(expected, result)
        with self.assertRaises(Exception):
            self.p._get_compound_name('MSR674_SET14REP15C3_INVALIDCOMPOUND_DIA.d')

    def test_get_batch_compound_names(self):
        data = {
            'Compound': ['MSR5863_SET10REP2C3_TAL123_DIA.d',
                         'MSR12_SET9REP14C3_TAL0000981_DIA.d',
                         'MSR10000_SET12REP3C3_TAL1052_DIA.d',
                         'MSR5864_SET14REP15C3_FRA00012_DIA.d'],
            'Other_Column': [1, 2, 3, 4]
        }
        pivot_df = pd.DataFrame(data).reset_index(drop=True)

        expected_df = pd.DataFrame({
            'Compound': ["TAL123", "TAL981", "TAL1052", "FRA"],
            'Other_Column': [1, 2, 3, 4],
            'batch': ['SET10REP2_Anborn', 
                      'SET9REP14_THP-1 1K',
                      'SET12REP3_Anborn',
                      'SET14REP15_Anborn']
        })

        result = self.p._get_batch_compound_names(pivot_df)

        result = result.reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)

        pd.testing.assert_frame_equal(result, expected_df)

class TestPeptideProcessor(unittest.TestCase):

    test_pr_path = os.path.join(os.getcwd(), "test", "test_pr_matrix.csv")
    test_pg_path = os.path.join(os.getcwd(), "test", "test_pg_matrix.csv")

    def setUp(self):
        self.pep_proc = PeptideProcessor()

    def test_process_and_normalize(self):
        data = {
            ('batch', '', ''): ['SET1REP1', 'SET1REP1', 'SET1REP1', 'SET1REP1', 'SET1REP1'],
            ('Compound', '', ''): ['FRA', 'FRA', 'FRA', 'TAL281', 'TAL1432'],
            ('P37108', 'SRP14', 'AAAAAAAAAPAAAATAPTTAATTAATAAQ3'): [-1.259301, None, -1.399689, 0.235722, 0.034296],
            ('Q96JP5;Q96JP5-2', 'ZFP91', 'AAAAAAAAAVSR2'): [None, 1.220315, None, 1.883378, 1.644666],
            ('P36578', 'RPL4', 'AAAAAAALQAK2'): [4.271176, 4.997890, 4.730296, 4.594354, 4.698532],
            ('Q6SPF0', 'SAMD1', 'AAAAAATAPPSPGPAQPGPR2'): [-0.048668, -0.452178, -0.167983, -0.884466, None],
            ('Q8WUQ7;Q8WUQ7-2', 'CACTIN', 'AAAAALSQQQSLQER2'): [0.530404, 0.328163, 0.338736, 0.115737, 0.264015],
            ('Q9P258', 'RCC2', 'AAAAAWEEPSSGNGTAR2'): [1.659520, 2.074172, 1.756539, 1.406870, 1.164262],
            ('Q9UPT8', 'ZC3H4', 'AAAAPAATTATPPPEGAPPQPGVHNLPVPTLFGTVK4'): [None, -2.387604, None, None, -0.482742],
            ('Q68DK7', 'MSL1', 'AAAAPAGGNPEQR2'): [None, None, None, -0.329615, None],
            ('Q96L91;Q96L91-2;Q96L91-3;Q96L91-5', 'EP400', 'AAAAPFQTSQASASAPR2'): [None, None, None, -0.396926, -0.130211],
            ('P52701;P52701-2;P52701-3', 'MSH6', 'AAAAPGASPSPGGDAAWSEAGPGPRPLAR3'): [-1.501962, None, None, None, None],
            ('screen', '', ''): ['Anborn', 'Anborn', 'Anborn', 'Anborn', 'Anborn'],
        }

        multi_index = pd.MultiIndex.from_tuples([
            ('batch', '', ''),
            ('Compound', '', ''),
            ('P37108', 'SRP14', 'AAAAAAAAAPAAAATAPTTAATTAATAAQ3'),
            ('Q96JP5;Q96JP5-2', 'ZFP91', 'AAAAAAAAAVSR2'),
            ('P36578', 'RPL4', 'AAAAAAALQAK2'),
            ('Q6SPF0', 'SAMD1', 'AAAAAATAPPSPGPAQPGPR2'),
            ('Q8WUQ7;Q8WUQ7-2', 'CACTIN', 'AAAAALSQQQSLQER2'),
            ('Q9P258', 'RCC2', 'AAAAAWEEPSSGNGTAR2'),
            ('Q9UPT8', 'ZC3H4', 'AAAAPAATTATPPPEGAPPQPGVHNLPVPTLFGTVK4'),
            ('Q68DK7', 'MSL1', 'AAAAPAGGNPEQR2'),
            ('Q96L91;Q96L91-2;Q96L91-3;Q96L91-5', 'EP400', 'AAAAPFQTSQASASAPR2'),
            ('P52701;P52701-2;P52701-3', 'MSH6', 'AAAAPGASPSPGGDAAWSEAGPGPRPLAR3'),
            ('screen', '', '')
        ], names=['Protein.Ids', 'Genes', 'Precursor.Id'])


        expected_df = pd.DataFrame(data)
        expected_df.columns = multi_index

        quant_cols = [col for col in expected_df.columns if col not in [('batch', '', ''), ('Compound', '', ''),('screen', '', '')]]
        expected_df[quant_cols] = expected_df[quant_cols].astype(float)

        dl = DataLoader()
        data = dl.load_data(self.test_pr_path)
        result = self.pep_proc.process_and_normalize(data)

        pd.testing.assert_frame_equal(result.iloc[:5], expected_df)

        # Test inheritance of the screen identifier
        custom_screen_split = {(0, 100): "Screen A",  
                                (100, 1e16): "Screen B"}
        p = PeptideProcessor(screen_split=custom_screen_split)
        self.assertEqual(p.screen_split, custom_screen_split)
        self.assertEqual(p._get_screen('MSR100_SET10REP2C3_TAL123_DIA.d'), "Screen B")
        self.assertEqual(p._get_screen('MSR50_SET10REP2C3_TAL123_DIA.d'), "Screen A")
        self.assertEqual(p._get_screen('MSR102_SET10REP2C3_TAL123_DIA.d'), "Screen B")

        # Test that it ignores screens when instructed
        p = PeptideProcessor(label_screens=False)
        df = p.process_and_normalize(data)
        self.assertTrue("screen" not in df.columns)

        # Test error handling for wrong file
        with self.assertRaises(Exception):
            data = dl.load_data(self.test_pg_path)
            p.process_and_normalize(data)
        
class TestProteinProcessor(unittest.TestCase):
    test_pg_path = os.path.join(os.getcwd(), "test", "test_pg_matrix.csv")
    test_pr_path = os.path.join(os.getcwd(), "test", "test_pr_matrix.csv")

    def setUp(self):
        self.prot_proc = ProteinProcessor()

    def test_process_and_normalize(self):
        data = {
            'Genes': ['A2ML1', 'A2ML1', 'A2ML1', 'A2ML1', 'A2ML1'],
            'batch': ['SET1REP1', 'SET1REP1', 'SET1REP1', 'SET1REP1', 'SET1REP1'],
            'Protein.Ids': ['A8K2U0', 'A8K2U0', 'A8K2U0', 'A8K2U0', 'A8K2U0'],
            'Compound': ['TAL281', 'TAL153', 'TAL750', 'TAL1045', 'TAL369'],
            'Abundance': [-0.268770, 0.237281, 0.731664, -0.524845, -0.662243],
            'screen': ['Anborn', 'Anborn', 'Anborn', 'Anborn', 'Anborn']
        }

        expected_df = pd.DataFrame(data)

        dl = DataLoader()
        data = dl.load_data(self.test_pg_path)
        result = self.prot_proc.process_and_normalize(data)

        pd.testing.assert_frame_equal(result.iloc[:5], expected_df)

        # Test inheritance of the screen identifier
        custom_screen_split = {(0, 100): "Screen A",  
                                (100, 1e16): "Screen B"}
        p = ProteinProcessor(screen_split=custom_screen_split)
        self.assertEqual(p.screen_split, custom_screen_split)
        self.assertEqual(p._get_screen('MSR100_SET10REP2C3_TAL123_DIA.d'), "Screen B")
        self.assertEqual(p._get_screen('MSR50_SET10REP2C3_TAL123_DIA.d'), "Screen A")
        self.assertEqual(p._get_screen('MSR102_SET10REP2C3_TAL123_DIA.d'), "Screen B")


        # Test that it ignores screens when instructed
        p = ProteinProcessor(label_screens=False)
        df = p.process_and_normalize(data)
        self.assertTrue("screen" not in df.columns)

        # Test error handling for wrong file
        with self.assertRaises(Exception):
            data = dl.load_data(self.test_pr_path)
            p.process_and_normalize(data)

class TestProteinZScoreCalculator(unittest.TestCase):

    test_pg_path = os.path.join(os.getcwd(), "test", "test_pg_matrix.csv")
    test_pr_path = os.path.join(os.getcwd(), "test", "test_pr_matrix.csv")

    def setUp(self):
        self.dl  = DataLoader()
        self.prot_proc = ProteinProcessor()
        self.raw_pg_data = self.dl.load_data(self.test_pg_path)
        self.processed_pg_data = self.prot_proc.process_and_normalize(self.raw_pg_data)
        self.z = ProteinZScoreCalculator()
    
    def test_compute_z_score(self):
        z_score = self.z.compute_z_score(self.processed_pg_data)

        data = {
            'screen': ["Anborn"] *5,
            'Genes': ['A2ML1', 'A2ML1', 'A2ML1', 'A2ML1', 'A2ML1'],
            'batch': ['SET1REP1', 'SET1REP1', 'SET1REP1', 'SET1REP1', 'SET1REP1'],
            'Protein.Ids': ['A8K2U0', 'A8K2U0', 'A8K2U0', 'A8K2U0', 'A8K2U0'],
            'Compound': ['TAL281', 'TAL153', 'TAL750', 'TAL1045', 'TAL369'],
            'Abundance': [-0.268770, 0.237281, 0.731664, -0.524845, -0.662243],
            'Z Score': [-0.770911, 0.680591, 2.098623, -1.505407, -1.899505],
            'med Z Score': [-0.770911, -0.295842, 2.098623, -1.505407, -1.899505]
        }

        expected_df = pd.DataFrame(data)

        pd.testing.assert_frame_equal(z_score.iloc[:5], expected_df)

        # Test error handling
        data = self.dl.load_data(self.test_pr_path)
        pp = PeptideProcessor()
        data = pp.process_and_normalize(data)
        with self.assertRaises(Exception):
            self.z.compute_z_score(data)

        # Test calculating without screen data
        data = self.processed_pg_data.drop(columns=["screen"])
        result = self.z.compute_z_score(data)
        expected_df = expected_df.drop(columns=["screen"])
        pd.testing.assert_frame_equal(result.iloc[:5], expected_df)

class TestPeptideZScoreCalculator(unittest.TestCase):
    test_pg_path = os.path.join(os.getcwd(), "test", "test_pg_matrix.csv")
    test_pr_path = os.path.join(os.getcwd(), "test", "test_pr_matrix.csv")

    def setUp(self):
        self.dl  = DataLoader()
        self.pep_proc = PeptideProcessor()
        self.raw_pr_data = self.dl.load_data(self.test_pr_path)
        self.processed_pr_data = self.pep_proc.process_and_normalize(self.raw_pr_data)
        self.z = PeptideZScoreCalculator()

    def test_calculate_z_score(self):
        data = {
            ('batch', '', ''): ['SET1REP1', 'SET1REP1', 'SET1REP1', 'SET1REP1', 'SET1REP1'],
            ('Compound', '', ''): ['FRA', 'FRA', 'FRA', 'TAL281', 'TAL1432'],
            ('P37108', 'SRP14', 'AAAAAAAAAPAAAATAPTTAATTAATAAQ3'): [-0.633648, None, -0.817097, 1.319951, 1.056741],
            ('Q96JP5;Q96JP5-2', 'ZFP91', 'AAAAAAAAAVSR2'): [None, -0.194224, None, 1.384308, 0.816015],
            ('P36578', 'RPL4', 'AAAAAAALQAK2'): [-0.144179, 1.927473, 1.164640, 0.777109, 1.074089],
            ('Q6SPF0', 'SAMD1', 'AAAAAATAPPSPGPAQPGPR2'): [1.519493, 0.481067, 1.212439, -0.631415, None],
            ('Q8WUQ7;Q8WUQ7-2', 'CACTIN', 'AAAAALSQQQSLQER2'): [-0.248740, -1.179475, -1.130815, -2.157081, -1.474688],
            ('Q9P258', 'RCC2', 'AAAAAWEEPSSGNGTAR2'): [-0.142098, 1.157632, 0.162009, -0.934032, -1.694490],
            ('Q9UPT8', 'ZC3H4', 'AAAAPAATTATPPPEGAPPQPGVHNLPVPTLFGTVK4'): [None, -3.852793, None, None, 1.648315],
            ('Q68DK7', 'MSL1', 'AAAAPAGGNPEQR2'): [None, None, None, 1.614477, None],
            ('Q96L91;Q96L91-2;Q96L91-3;Q96L91-5', 'EP400', 'AAAAPFQTSQASASAPR2'): [None, None, None, -3.155988, -1.981292],
            ('P52701;P52701-2;P52701-3', 'MSH6', 'AAAAPGASPSPGGDAAWSEAGPGPRPLAR3'): [0.062269, None, None, None, None],
            ('screen', '', ''): ['Anborn', 'Anborn', 'Anborn', 'Anborn', 'Anborn']
        }

        multi_index = pd.MultiIndex.from_tuples([
            
            ('screen', '', ''),
            ('batch', '', ''),
            ('Compound', '', ''),
            ('P37108', 'SRP14', 'AAAAAAAAAPAAAATAPTTAATTAATAAQ3'),
            ('Q96JP5;Q96JP5-2', 'ZFP91', 'AAAAAAAAAVSR2'),
            ('P36578', 'RPL4', 'AAAAAAALQAK2'),
            ('Q6SPF0', 'SAMD1', 'AAAAAATAPPSPGPAQPGPR2'),
            ('Q8WUQ7;Q8WUQ7-2', 'CACTIN', 'AAAAALSQQQSLQER2'),
            ('Q9P258', 'RCC2', 'AAAAAWEEPSSGNGTAR2'),
            ('Q9UPT8', 'ZC3H4', 'AAAAPAATTATPPPEGAPPQPGVHNLPVPTLFGTVK4'),
            ('Q68DK7', 'MSL1', 'AAAAPAGGNPEQR2'),
            ('Q96L91;Q96L91-2;Q96L91-3;Q96L91-5', 'EP400', 'AAAAPFQTSQASASAPR2'),
            ('P52701;P52701-2;P52701-3', 'MSH6', 'AAAAPGASPSPGGDAAWSEAGPGPRPLAR3'),
        ], names=['Protein.Ids', 'Genes', 'Precursor.Id'])

        expected_df = pd.DataFrame(data, columns=multi_index)
        
        z_scores = self.z.compute_z_score(self.processed_pr_data)

        pd.testing.assert_frame_equal(z_scores.iloc[:5], expected_df)

        # Test error handling
        data = self.dl.load_data(self.test_pg_path)
        pp = ProteinProcessor()
        data = pp.process_and_normalize(data)
        with self.assertRaises(Exception):
            self.z.compute_z_score(data)

        # Test calculating without screen data
        data = self.processed_pr_data.drop(columns=["screen"])
        result = self.z.compute_z_score(data)
        expected_df = expected_df.drop(columns=["screen"])
        pd.testing.assert_frame_equal(result.iloc[:5], expected_df)

    def test_get_median_z_score(self):
        data = {
            ('screen', '', ''): ['Anborn', 'Anborn', 'Anborn', 'Anborn', 'Anborn'],
            ('Compound', '', ''): ['DMSO', 'FRA', 'TAL1025', 'TAL1035', 'TAL1036'],
            ('P37108', 'SRP14', 'AAAAAAAAAPAAAATAPTTAATTAATAAQ3'): [-0.5334404597266602, -1.065759928730299, -1.14072170539318, -1.1491300791676362, 0.7934110550949246],
            ('Q96JP5;Q96JP5-2', 'ZFP91', 'AAAAAAAAAVSR2'): [0.010751789897853276, -1.3941499110509465, -1.4619871104404696, -1.7771470859195677, 0.2951661994836766],
            ('P36578', 'RPL4', 'AAAAAAALQAK2'): [-0.08901027512310429, 0.18773835192781038, -1.7527948875349475, -2.748797162058653, 0.4322621634948626],
            ('Q6SPF0', 'SAMD1', 'AAAAAATAPPSPGPAQPGPR2'): [0.30054259069394285, -0.052905785507017494, -0.26482233093935587, 1.116107963009016, -2.934392700758811],
            ('Q8WUQ7;Q8WUQ7-2', 'CACTIN', 'AAAAALSQQQSLQER2'): [-0.2698689815435681, 1.6589867932303823, 0.34527420814361953, 1.2045920625074742, -0.23144935753882287],
            ('Q9P258', 'RCC2', 'AAAAAWEEPSSGNGTAR2'): [0.22423292436539943, -0.846004020837186, 0.9249935779133865, 0.3857646051171687, -1.7044456467273803],
            ('Q9UPT8', 'ZC3H4', 'AAAAPAATTATPPPEGAPPQPGVHNLPVPTLFGTVK4'): [-0.06374910333421302, -2.941365586022088, -0.23130436913780278, -0.10268224834794583, 0.3246818145759337],
            ('Q68DK7', 'MSL1', 'AAAAPAGGNPEQR2'): [0.20173751892825315, None, -1.0820230224411604, -0.8993800988528352, 2.3200731275682895],
            ('Q96L91;Q96L91-2;Q96L91-3;Q96L91-5', 'EP400', 'AAAAPFQTSQASASAPR2'): [0.014440016001873753, -7.402101520381838, -0.0726318618271808, 1.563459708454522, -0.5600934040856896],
            ('P52701;P52701-2;P52701-3', 'MSH6', 'AAAAPGASPSPGGDAAWSEAGPGPRPLAR3'): [0.7226367290294418, -0.7149719326926692, 0.4589032324230374, 0.0746398178336411, None],
        }

        multi_index = pd.MultiIndex.from_tuples(
            [('screen', '', ''),
            ('Compound', '', ''),
            ('P37108', 'SRP14', 'AAAAAAAAAPAAAATAPTTAATTAATAAQ3'),
            ('Q96JP5;Q96JP5-2', 'ZFP91', 'AAAAAAAAAVSR2'),
            ('P36578', 'RPL4', 'AAAAAAALQAK2'),
            ('Q6SPF0', 'SAMD1', 'AAAAAATAPPSPGPAQPGPR2'),
            ('Q8WUQ7;Q8WUQ7-2', 'CACTIN', 'AAAAALSQQQSLQER2'),
            ('Q9P258', 'RCC2', 'AAAAAWEEPSSGNGTAR2'),
            ('Q9UPT8', 'ZC3H4', 'AAAAPAATTATPPPEGAPPQPGVHNLPVPTLFGTVK4'),
            ('Q68DK7', 'MSL1', 'AAAAPAGGNPEQR2'),
            ('Q96L91;Q96L91-2;Q96L91-3;Q96L91-5', 'EP400', 'AAAAPFQTSQASASAPR2'),
            ('P52701;P52701-2;P52701-3', 'MSH6', 'AAAAPGASPSPGGDAAWSEAGPGPRPLAR3')]
            , names=['Protein.Ids', 'Genes', 'Precursor.Id'])

        expected_df = pd.DataFrame(data, columns=multi_index)

        z_scores = self.z.compute_z_score(self.processed_pr_data)
        result = self.z.get_median_z_score(z_scores)
        pd.testing.assert_frame_equal(result.iloc[:5], expected_df)
    
    def test_melt_z_score_df(self):
        data = {
            'screen': ['Anborn', 'Anborn', 'Anborn', 'Anborn', 'Anborn'],
            'batch': ['SET1REP1', 'SET1REP1', 'SET1REP1', 'SET1REP1', 'SET1REP1'],
            'Compound': ['FRA', 'FRA', 'FRA', 'TAL281', 'TAL1432'],
            'Abundance': [-0.633648, np.nan, -0.817097, 1.319951, 1.056741],
            'Protein.Ids': ['P37108', 'P37108', 'P37108', 'P37108', 'P37108'],
            'Genes': ['SRP14', 'SRP14', 'SRP14', 'SRP14', 'SRP14'],
            'Precursor.Id': ['AAAAAAAAAPAAAATAPTTAATTAATAAQ3'] * 5  
        }

        expected_df = pd.DataFrame(data)

        z_scores = self.z.compute_z_score(self.processed_pr_data)
        result = self.z.melt_z_score_df(z_scores)
        pd.testing.assert_frame_equal(result.iloc[:5], expected_df)



if __name__ == '__main__':
    unittest.main(warnings="ignore")