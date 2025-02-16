from domain.icontent_out import IContentOut
from typing import List, Dict

class ContentOut(IContentOut):
    
    def __init__(self):  
        pass

    def set_base_file_name(self, out_file_name: str) -> None:
        self.out_file_name = out_file_name
        with open(self.out_file_name, "w", encoding="utf-8") as file:            
            file.write('')    

    def write(self, lines: List) -> None:
        with open(self.out_file_name, "a", encoding="utf-8") as file:            
            file.write('\n'.join(lines))

