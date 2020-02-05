'''
Created on Apr 10, 2019

@author: janmeyer
'''

from enum import IntEnum
from PyQt5.QtGui import QColor

class UpdatePolicy(IntEnum):
    NO = 0
    POLLING = 1
    EVENTBASED = 2

class State(IntEnum):
    ON = 0
    OFF = 1
    CLOSE = 2
    OPEN = 3
    INSERT = 4
    EXTRACT = 5
    MOVING = 6
    STANDBY = 7
    FAULT = 8
    INIT = 9
    RUNNING = 10
    ALARM = 11
    DISABLE = 12
    UNKNOWN = 13

def StateColor(state):
    values = ( \
        StateColor.ON,
        StateColor.OFF,
        StateColor.CLOSE,
        StateColor.OPEN,
        StateColor.INSERT,
        StateColor.EXTRACT,
        StateColor.MOVING,
        StateColor.STANDBY,
        StateColor.FAULT,
        StateColor.INIT,
        StateColor.RUNNING,
        StateColor.ALARM,
        StateColor.DISABLE,
        StateColor.UNKNOWN,
    )
    return values[int(state)]
StateColor.ON = QColor(0, 255, 0)          #Green
StateColor.OFF = QColor(255, 255, 255)     #White
StateColor.CLOSE = QColor(255, 255, 255)   #White
StateColor.OPEN = QColor(0, 255, 0)        #Green
StateColor.INSERT = QColor(255, 255, 255)  #White
StateColor.EXTRACT = QColor(0, 255, 0)     #Green
StateColor.MOVING = QColor(128, 160, 255)  #Light Blue
StateColor.STANDBY = QColor(255, 255, 0)   #Yellow
StateColor.FAULT = QColor(255, 0, 0)       #Red
StateColor.INIT = QColor(204, 204, 122)    #Beige
StateColor.RUNNING = QColor(0, 125, 0)     #Dark Green
StateColor.ALARM = QColor(255, 140, 0)     #Orange
StateColor.DISABLE = QColor(255, 0, 255)   #Magenta
StateColor.UNKNOWN = QColor(155, 155, 155) #Grey


def ChemicalElement(z):
    # Sources:
    #X-Ray Data Booklet, http://xdb.lbl.gov/xdb.pdf
    #https://www.amptek.com/resources/periodic-table-and-x-ray-emission-line-lookup-chart
    #https://physics.nist.gov/PhysRefData/XrayTrans/Html/search.html
    elements = [ \
        ["z", "symbol", "name", "k_edge", "l1_edge", "l2_edge", "l3_edge",
            "k_alpha1", "k_alpha2", "k_beta1", "l_alpha1", "l_alpha2", 
            "l_beta1", "l_beta2", "l_gamma1"],
        [1, "H", "Hydrogen", 13.6, None, None, None,
            None, None, None, None, None, None, None, None],
        [2, "He", "Helium", 24.6, None, None, None,
            None, None, None, None, None, None, None, None],
        [3, "Li", "Lithium", 54.7, None, None, None,
            54.3, None, None, None, None, None, None, None],
        [4, "Be", "Beryllium", 111.5, None, None, None,
            108.5, None, None, None, None, None, None, None],
        [5, "B", "Boron", 188, None, None, None,
            183.3, None, None, None, None, None, None, None],
        [6, "C", "Carbon", 284.2, None, None, None,
            277, None, None, None, None, None, None, None],
        [7, "N", "Nitrogen", 409.9, 37.3, None, None,
            392.4, None, None, None, None, None, None, None],
        [8, "O", "Oxygen", 543.1, 41.6, None, None,
            524.9, None, None, None, None, None, None, None],
        [9, "F", "Fluorine", 696.7, None, None, None,
            676.8, None, None, None, None, None, None, None],
        [10, "Ne", "Neon", 870.2, 48.5, 21.7, 21.6,
            848.6, 848.6, None, None, None, None, None, None],
        [11, "Na", "Sodium", 1070.8, 63.5, 30.65, 30.81,
            1040.98, 1040.98, 1071.1, None, None, None, None, None],
        [12, "Mg", "Magnesium", 1303, 88.7, 49.78, 49.5,
            1253.6, 1253.6, 1302.2, None, None, None, None, None],
        [13, "Al", "Aluminium", 1559.6, 117.8, 72.95, 72.55,
            1486.7, 1486.27, 1557.45, None, None, None, None, None],
        [14, "Si", "Silicon", 1839, 149.7, 99.82, 99.42,
            1739.98, 1739.38, 1835.94, None, None, None, None, None],
        [15, "P", "Phosphorus", 2145.5, 189, 136, 135,
            2013.7, 2012.7, 2139.1, None, None, None, None, None],
        [16, "S", "Sulfur", 2472, 230.9, 163.6, 162.5,
            2307.84, 2306.64, 2464.04, None, None, None, None, None],
        [17, "Cl", "Chlorine", 2822.4, 270, 202, 200,
            2622.39, 2620.78, 2815.6, None, None, None, None, None],
        [18, "Ar", "Argon", 3205.9, 326.3, 250.6, 248.4,
            2957.7, 2955.63, 3190.5, None, None, None, None, None],
        [19, "K", "Potassium", 3608.4, 378.6, 297.3, 294.6,
            3313.8, 3311.1, 3589.6, None, None, None, None, None],
        [20, "Ca", "Calcium", 4038.5, 438.4, 349.7, 346.2,
            3691.68, 3688.09, 4012.7, 341.3, 341.3, 344.9, None, None],
        [21, "Sc", "Scandium", 4492, 498, 403.6, 398.7,
            4090.6, 4086.1, 4460.5, 395.4, 395.4, 399.6, None, None],
        [22, "Ti", "Titanium", 4966, 560.9, 460.2, 453.8,
            4510.84, 4504.86, 4931.81, 452.2, 452.2, 458.4, None, None],
        [23, "V", "Vanadium", 5465, 626.7, 519.8, 512.1,
            4952.2, 4944.64, 5427.29, 511.3, 511.3, 519.2, None, None],
        [24, "Cr", "Chromium", 5989, 696, 583.8, 574.1,
            5414.72, 5405.509, 5946.71, 572.8, 572.8, 582.8, None, None],
        [25, "Mn", "Manganese", 6539, 769.1, 649.9, 638.7,
            5898.75, 5887.65, 6490.45, 637.4, 637.4, 648.8, None, None],
        [26, "Fe", "Iron", 7112, 844.6, 719.9, 706.8,
            6403.84, 6390.84, 7057.98, 705, 705, 718.5, None, None],
        [27, "Co", "Cobalt", 7709, 925.1, 793.2, 778.1,
            6930.32, 6915.3, 7649.43, 776.2, 776.2, 791.4, None, None],
        [28, "Ni", "Nickel", 8333, 1008.6, 870, 852.7,
            7478.15, 7460.89, 8264.66, 851.5, 851.5, 868.8, None, None],
        [29, "Cu", "Copper", 8979, 1096.7, 952.3, 932.7,
            8047.78, 8027.83, 8905.29, 929.7, 929.7, 949.8, None, None],
        [30, "Zn", "Zinc", 9659, 1196.2, 1044.9, 1021.8,
            8638.86, 8615.78, 9572, 1011.7, 1011.7, 1034.7, None, None],
        [31, "Ga", "Gallium", 10367, 1299, 1143.2, 1116.4,
            9251.74, 9224.82, 10264.2, 1097.92, 1097.92, 1124.8, None, None],
        [32, "Ge", "Germanium", 11103, 1414.6, 1248.1, 1217,
            9886.42, 9855.32, 10982.1, 1188, 1188, 1218.5, None, None],
        [33, "As", "Arsenic", 11867, 1527, 1359.1, 1323.6,
            10543.72, 10507.99, 11726.2, 1282, 1282, 1317, None, None],
        [34, "Se", "Selenium", 12658, 1652, 1474.3, 1433.9,
            11222.4, 11181.4, 12495.9, 1379.1, 1379.1, 1419.23, None, None],
        [35, "Br", "Bromine", 13474, 1782, 1596, 1550,
            11924.2, 11877.6, 13291.4, 1480.43, 1480.43, 1525.9, None, None],
        [36, "Kr", "Krypton", 14326, 1921, 1730.9, 1678.4,
            12649, 12598, 14112, 1586, 1586, 1636.6, None, None],
        [37, "Rb", "Rubidium", 15200, 2065, 1864, 1804,
            13395.3, 13335.8, 14961.3, 1694.13, 1692.56, 1752.17, None, None],
        [38, "Sr", "Strontium", 16105, 2216, 2007, 1940,
            14165, 14097.9, 15835.7, 1806.56, 1804.74, 1871.72, None, None],
        [39, "Y", "Yttrium", 17038, 2373, 2156, 2080,
            14958.4, 14882.9, 16737.8, 1922.56, 1920.47, 1995.84, None, None],
        [40, "Zr", "Zirconium", 17998, 2532, 2307, 2223,
            15775.1, 15690.9, 17667.8, 2042.36, 2039.9, 2124.4, 2219.4, 2302.7],
        [41, "Nb", "Niobium", 18986, 2698, 2465, 2371,
            16615.1, 16521, 18622.5, 2165.89, 2163, 2257.4, 2367, 2461.8],
        [42, "Mo", "Molybdenum", 20000, 2866, 2625, 2520,
            17479.34, 17374.3, 19608.3, 2293.16, 2289.85, 2394.81, 2518.3, 2623.5],
        [43, "Tc", "Technetium", 21044, 3043, 2793, 2677,
            18367.1, 18250.8, 20619, 2424, 2420, 2538, 2674, 2792],
        [44, "Ru", "Ruthenium", 22117, 3224, 2967, 2838,
            19279.2, 19150.4, 21656.8, 2558.55, 2554.31, 2683.23, 2836, 2964.5],
        [45, "Rh", "Rhodium", 23220, 3412, 3146, 3004,
            20216.1, 20073.7, 22723.6, 2696.74, 2692.05, 2834.41, 3001.3, 3143.8],
        [46, "Pd", "Palladium", 24350, 3604, 3330, 3173,
            21177.1, 21020.1, 23818.7, 2838.61, 2833.29, 2990.22, 3171.79, 3328.7],
        [47, "Ag", "Silver", 25514, 3806, 3524, 3351,
            22162.92, 21990.3, 24942.4, 2984.31, 2978.21, 3150.94, 3347.81, 3519.59],
        [48, "Cd", "Cadmium", 26711, 4018, 3727, 3538,
            23173.6, 22984.1, 26095.5, 3133.73, 3126.91, 3316.57, 3528.12, 3716.86],
        [49, "In", "Indium", 27940, 4238, 3938, 3730,
            24209.7, 24002, 27275.9, 3286.94, 3279.29, 3487.21, 3713.81, 3920.81],
        [50, "Sn", "Tin", 29200, 4465, 4156, 3929,
            25271.3, 25044, 28486, 3443.98, 3435.42, 3662.8, 3904.86, 4131.12],
        [51, "Sb", "Antimony", 30491, 4698, 4380, 4132,
            26359.1, 26110.8, 29725.6, 3604.72, 3595.32, 3843.57, 4100.78, 4347.79],
        [52, "Te", "Tellurium", 31814, 4939, 4612, 4341,
            27472.3, 27201.7, 30995.7, 3769.33, 3758.8, 4029.58, 4301.7, 4570.9],
        [53, "I", "Iodine", 33169, 5188, 4852, 4557,
            28612, 28317.2, 32294.7, 3937.65, 3926.04, 4220.72, 4507.5, 4800.9],
        [54, "Xe", "Xenon", 34561, 5453, 5107, 4786,
            29779, 29458, 33624, 4109.9, None, 4418, None, None],
        [55, "Cs", "Caesium", 35985, 5714, 5359, 5012,
            30972.8, 30625.1, 34986.9, 4286.5, 4272.2, 4619.8, 4935.9, 5280.4],
        [56, "Ba", "Barium", 37441, 5989, 5624, 5247,
            32193.6, 31817.1, 36378.2, 4466.26, 4450.9, 4827.53, 5156.5, 5531.1],
        [57, "La", "Lanthanum", 38925, 6266, 5891, 5483,
            33441.8, 33034.1, 37801, 4650.97, 4634.23, 5042.1, 5383.5, 5788.5],
        [58, "Ce", "Cerium", 40443, 6549, 6164, 5723,
            34719.7, 34278.9, 39257.3, 4840.2, 4823, 5262.2, 5613.4, 6052],
        [59, "Pr", "Praseodymium", 41991, 6835, 6440, 5964,
            36026.3, 35550.2, 40748.2, 5033.7, 5013.5, 5488.9, 5850, 6322.1],
        [60, "Nd", "Neodymium", 43569, 7126, 6722, 6208,
            37361, 36847.4, 42271.3, 5230.4, 5207.7, 5721.6, 6089.4, 6602.1],
        [61, "Pm", "Promethium", 45184, 7428, 7013, 6459,
            38724.7, 38171.2, 43826, 5432.5, 5407.8, 5961, 6339, 6892],
        [62, "Sm", "Samarium", 46834, 7737, 7312, 6716,
            40118.1, 39522.4, 45413, 5636.1, 5609, 6205.1, 6586, 7178],
        [63, "Eu", "Europium", 48519, 8052, 7617, 6977,
            41542.2, 40901.9, 47037.9, 5845.7, 5816.6, 6456.4, 6843.2, 7480.3],
        [64, "Gd", "Gadolinium", 50239, 8376, 7930, 7243,
            42996.2, 42308.9, 48697, 6057.2, 6025, 6713.2, 7102.8, 7785.8],
        [65, "Tb", "Terbium", 51996, 8708, 8252, 7514,
            44481.6, 43744.1, 50382, 6272.8, 6238, 6978, 7366.7, 8102],
        [66, "Dy", "Dysprosium", 53789, 9046, 8581, 7790,
            45998.4, 45207.8, 52119, 6495.2, 6457.7, 7247.7, 7635.7, 8418.8],
        [67, "Ho", "Holmium", 55618, 9394, 8918, 8071,
            47546.7, 46699.7, 53877, 6719.8, 6679.5, 7525.3, 7911, 8747],
        [68, "Er", "Erbium", 57486, 9751, 9264, 8358,
            49127.7, 48221.1, 55681, 6948.7, 6905, 7810.9, 8189, 9089],
        [69, "Tm", "Thulium", 59390, 10116, 9617, 8648,
            50741.6, 49772.6, 57517, 7179.9, 7133.1, 8101, 8468, 9426],
        [70, "Yb", "Ytterbium", 61332, 10486, 9978, 8944,
            52388.9, 51354, 59370, 7415.6, 7367.3, 8401.8, 8758.8, 9780.1],
        [71, "Lu", "Lutetium", 63314, 10870, 10349, 9244,
            54069.8, 52965, 61283, 7655.5, 7604.9, 8709, 9048.9, 10143.4],
        [72, "Hf", "Hafnium", 65351, 11271, 10739, 9561,
            55790.2, 54611.4, 63234, 7899, 7844.6, 9022.7, 9347.3, 10515.8],
        [73, "Ta", "Tantalum", 67416, 11682, 11136, 9881,
            57532, 56277, 65223, 8146.1, 8087.9, 9343.1, 9651.8, 10895.2],
        [74, "W", "Tungsten", 69525, 12100, 11544, 10207,
            59318.24, 57981.7, 67244.3, 8397.6, 8335.2, 9672.35, 9961.5, 11285.9],
        [75, "Re", "Rhenium", 71676, 12527, 11959, 10535,
            61140.3, 59717.9, 69310, 8652.5, 8586.2, 10010, 10275.2, 11685.4],
        [76, "Os", "Osmium", 73871, 12968, 12385, 10871,
            63000.5, 61486.7, 71413, 8911.7, 8841, 10355.3, 10598.5, 12095.3],
        [77, "Ir", "Iridium", 76111, 13419, 12824, 11215,
            64895.6, 63286.7, 73560.8, 9175.1, 9099.5, 10708.3, 10920.3, 12512.6],
        [78, "Pt", "Platinum", 78395, 13880, 13273, 11564,
            66832, 65112, 75748, 9442.3, 9361.8, 11070.7, 11250.5, 12942],
        [79, "Au", "Gold", 80725, 14353, 13734, 11919,
            68803.7, 66989.5, 77984, 9713.3, 9628, 11442.3, 11584.7, 13381.7],
        [80, "Hg", "Mercury", 83102, 14839, 14209, 12284,
            70819, 68895, 80253, 9988.8, 9897.6, 11822.6, 11924.1, 13830.1],
        [81, "Tl", "Thallium", 85530, 15347, 14698, 12658,
            72871.5, 70831.9, 82576, 10268.5, 10172.8, 12213.3, 12271.5, 14291.5],
        [82, "Pb", "Lead", 88005, 15861, 15200, 13035,
            74969.4, 72804.2, 84936, 10551.5, 10449.5, 12613.7, 12622.6, 14764.4],
        [83, "Bi", "Bismuth", 90524, 16388, 15711, 13419,
            77107.9, 74814.8, 87343, 10838.8, 10730.91, 13023.5, 12979.9, 15247.7],
        [84, "Po", "Polonium", 93105, 16939, 16244, 13814,
            79290, 76862, 89800, 11130.8, 11015.8, 13447, 13340.4, 15744],
        [85, "At", "Astatine", 95730, 17493, 16785, 14214,
            81520, 78950, 92300, 11426.8, 11304.8, 13876, None, 16251],
        [86, "Rn", "Radon", 98404, 18049, 17337, 14619,
            83780, 81070, 94870, 11727, 11597.9, 14316, None, 16770],
        [87, "Fr", "Francium", 101137, 18639, 17907, 15031,
            86100, 83230, 97470, 12031.3, 11895, 14770, 14450, 17303],
        [88, "Ra", "Radium", 103922, 19237, 18484, 15444,
            88470, 85430, 100130, 12339.7, 12196.2, 15235.8, 14841.4, 17849],
        [89, "Ac", "Actinium", 106755, 19840, 19083, 15871,
            90884, 87670, 102850, 12652, 12500.8, 15713, None, 18408],
        [90, "Th", "Thorium", 109651, 20472, 19693, 16300,
            93350, 89953, 105609, 12968.7, 12809.6, 16202.2, 15623.7, 18982.5],
        [91, "Pa", "Protactinium", 112601, 21105, 20314, 16733,
            95868, 92287, 108427, 13290.7, 13122.2, 16702, 16024, 19568],
        [92, "U", "Uranium", 115606, 21757, 20948, 17166,
            98439, 94665, 111300, 13614.7, 13438.8, 17220, 16428.3, 20167.1],
        [93, "Np", "Neptunium", 118688.7, 22437.5, 21615, 17608.04,
            101000, None, 114180, 13944.1, 13759.7, 17750.2, 16840, 20784.8],
        [94, "Pu", "Plutonium", 121790.17, 23113, 22251, 18055.99,
            103650, None, 117150, 14278.6, 14084.2, 18293.7, 17255.3, 21417.3],
        [95, "Am", "Americium", 124986.1, 23808, 22952.0, 18510,
            106350, None, 120160, 14617.2, 14411.9, 18852, 17676.5, 22065.2],
        [96, "Cm", "Curium", 128241.3, 24515, 23651, 18970,
            109100, None, 123240, 14960, None, 19390, None, None],
        [97, "Bk", "Berkelium", 131555.6, 25272, 24382, 19449,
            111900, None, 126360, 15310, None, 19970, None, None],
        [98, "Cf", "Californium", 134935.4, 26002.39, 25097.79, 19901.45,
            114750, None, 129540, 15660, None, 20560, None, None],
        [99, "Es", "Einsteinium", 138391.5, 26792.1, 25869.90, 20389.42,
            117650, None, 132780, 16020, None, 21170, None, None],
        [100, "Fm", "Fermium", 141930.4, 27573.0, 26644.0, 20868,
            120600, None, 136080, 16380, None, 21790, None, None],
        [101, "Md", "Mendelevium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [102, "No", "Nobelium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [103, "Lr", "Lawrencium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [104, "Rf", "Rutherfordium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [105, "Db", "Dubnium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [106, "Sg", "Seaborgium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [107, "Bh", "Bohrium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [108, "Hs", "Hassium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [109, "Mt", "Meitnerium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [110, "Ds", "Darmstadtium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [111, "Rg", "Roentgenium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [112, "Cn", "Copernicium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [113, "Nh", "Nihonium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [114, "Fl", "Flerovium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [115, "Mc", "Moscovium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [116, "Lv", "Livermorium", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [117, "Ts", "Tennessine", None, None, None, None,
            None, None, None, None, None, None, None, None],
        [118, "Og", "Oganesson", None, None, None, None,
            None, None, None, None, None, None, None, None],
        ]
    element = getattr(ChemicalElement, elements[z][1].upper(), None)
    if element is None and z > 0 and z < len(elements):
        element = type("Element", (object,), {})
        for i in range(len(elements[z])):
            if elements[z][i] is not None:
                setattr(element, elements[0][i], elements[z][i])
        setattr(ChemicalElement, element.symbol.upper(), element)
    return element
for z in range(1, 119):
    ChemicalElement(z)

