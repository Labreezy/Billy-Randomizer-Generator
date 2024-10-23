from geckolibs.gct import *
from geckolibs.geckocode import *
import random

def mission_name_to_bytestring(mission_name : str):
    return mission_name.encode("utf-8").ljust(8,b'\x00')

def shuffle_all_except(lst : list, except_list=[]):

    except_indices = [lst.index(exc) for exc in except_list]
    if len(except_indices) == 0:
        random.shuffle(lst)
        return lst
    sorted(except_indices)

    indices = [i for i in range(len(lst)) if i not in except_indices]
    random.shuffle(indices)
    for e in except_indices:
        indices.insert(e,e)
    shuffled_lst = [lst[i] for i in indices]
    return shuffled_lst

class CodeGenerator:
    def __init__(self):
        self.WORLD_NAMES = ['blue','red','purple','orange','yellow','green','last']
        self.WORLDS_BASE = 0x802CB5B0

        self.WORLD_TABLE_BASES = [self.WORLDS_BASE + i * 64 for i in range(len(self.WORLD_NAMES))]
        self.MISSION_NAMES_BILLY = []
        self.MISSION_NAMES_ROLLY = [wname + "6" for wname in self.WORLD_NAMES]
        self.MISSION_NAMES_CHICK = [wname + "7" for wname in self.WORLD_NAMES]
        self.MISSION_NAMES_BANTAM = [wname + "8" for wname in self.WORLD_NAMES]
        self.SEED = 0
        self.code = None
        self.gct = GeckoCodeTable("GEZE8P", "Billy Hatcher and the Giant Egg")
        self.gct_filename = ""
        for world in self.WORLD_NAMES:
            for i in range(5):
                if world == "last" and i == 0:
                    self.MISSION_NAMES_BILLY.append("last")
                else:
                    self.MISSION_NAMES_BILLY.append(f"{world}{i+1}")
    
    def gen_code(self, seed=-1):
        if seed < 0:
            self.SEED = random.randint(1,65535)
        else:
            self.SEED = seed
        random.seed(self.SEED)
        self.gct_filename = f"GEZE8P_seed_{seed}.gct"
        self.MISSION_NAMES_BILLY = shuffle_all_except(self.MISSION_NAMES_BILLY, ['yellow3', 'last'])
        random.shuffle(self.MISSION_NAMES_ROLLY)
        random.shuffle(self.MISSION_NAMES_CHICK)
        random.shuffle(self.MISSION_NAMES_BANTAM)
        MISSION_OUT_TABLE = []
        for i in range(len(self.WORLD_NAMES)):
            MISSION_OUT_TABLE +=self.MISSION_NAMES_BILLY[i * 5:(i + 1) * 5]
            MISSION_OUT_TABLE.append(self.MISSION_NAMES_ROLLY[i])
            MISSION_OUT_TABLE.append(self.MISSION_NAMES_CHICK[i])
            MISSION_OUT_TABLE.append(self.MISSION_NAMES_BANTAM[i])
        MISSION_OUT_TABLE_BYTES = b"".join(list(map(mission_name_to_bytestring, MISSION_OUT_TABLE)))
        self.code = WriteString(MISSION_OUT_TABLE_BYTES, self.WORLDS_BASE)
        self.code = GeckoCode(f"Billy Rando Seed {self.SEED}", "Labrys","Rando v0.0.2", self.code)

    def get_code_text(self):
        if self.code is not None:
            return self.code.as_text()
        return ""

    def get_gct_bytes(self):
        if self.code is not None:
            self.gct = GeckoCodeTable("GEZE8P", "Billy Hatcher and the Giant Egg")
            self.gct.add_child(self.code)
            return self.gct.as_bytes()
        else:
            return b""
