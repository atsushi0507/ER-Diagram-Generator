import os
import argparse
import pandas as pd

from utils import make_excel

class ERDiagram:
    def __init__(self, title="Sample Diagram"):
        self.title = title
        self.obj = f"```plantuml\n@startuml\ntitle {self.title}\n"
        self.relation = f"```plantuml\n@startuml\ntop to bottom direction\n"
        self.note = f"```plantuml\n@startuml\n"


    def make_entity(self, entity_name, primary_keys=None, foreign_keys=None, url=None):
        if str(url) != "nan":
            self.obj += f"entity {entity_name} [[{url}]]" + "{\n"
        else:
            self.obj += f"entity {entity_name}" + "{\n"
        if primary_keys is not None:
            if type(primary_keys) == str:
                self.obj += f"* {primary_keys} [PK]\n"
            else:
                for key in primary_keys:
                    self.obj += f"+ {key} [PK]\n"
        self.obj += "--\n"
        if foreign_keys is not None:
            if type(foreign_keys) == str:
                self.obj += f"{foreign_keys} [FK]\n"
            else:
                for key in foreign_keys:
                    self.obj += f"{key} [FK]\n"
        self.obj += "}\n"

    
    def make_relation(self, parent, child, description):
        arrow = "--|>"
        to_join = "--"
        note_to_join = "--left--"
        to_process = "--"
        if "join" in child:
            self.relation += f"{parent} {to_join} {child}\n"
            if str(description) != "nan":
                self.relation += f"note_{parent}_{child} {note_to_join} {child}\n"
        else:
            if str(description) != "nan":
                self.relation += f"{parent} {to_process} note_{parent}_{child}\n"
                self.relation += f"note_{parent}_{child} {arrow} {child}\n"

    def make_marker(self, child):
        if "join" in child:
            print(child)

    
    def make_note(self, parent, child, description):
        if not str(description) == "nan":
            self.note += f"note as note_{parent}_{child} #BurlyWood\n"
            self.note += f"{description}\n"
            self.note += "end note\n\n"


    def load_table(self, load_file):
        self.relation += f"!include ../tables/{load_file}\n\n"


    def load_note(self, load_file):
        self.relation += f"!include ../notes/note-{load_file}\n\n"


    def make_entities_from_excel(self, filename):
        book = pd.ExcelFile(filename)
        sheets = book.sheet_names
        for sheet_name in sheets:
            if sheet_name == "relation" or sheet_name == "process":
                continue
            df = book.parse(sheet_name=sheet_name, index_col=0)
            try:
                url = df.URL.iloc[0]
            except IndexError as e:
                print(f"URL is not specified for table: {sheet_name}")
                url = None

            df_dict = df.to_dict()
            PKs = []
            FKs = []
            vars = []
            comments = []
            for key, values in df_dict.items():
                for k, value in values.items():
                    if key == "Primary Key" and value == 1.0:
                        PKs.append(k)
                    elif key == "Foreign Key" and value == 1.0:
                        FKs.append(k)

            if len(PKs) == 0:
                PKs = None
            if len(FKs) == 0:
                FKs = None
            if len(vars) == 0:
                vars = None

            self.make_entity(sheet_name, PKs, FKs, url)
        self.output_table(f"{filename.split('.')[-2]}.md")


    def make_relations_from_excel(self, filename, load_file):
        book = pd.ExcelFile(filename)
        if load_file is not None:
            self.load_table(f"{load_file}")
            self.load_note(f"{load_file}")

        df = book.parse(sheet_name="relation")

        parents = df.From.to_list()
        children = df.To.to_list()
        descriptions = df.Description.to_list()

        markers = []
        for child in children:
            if "join" in child and child not in markers:
                markers.append(child)
        for marker in markers:
            self.relation += f"() {marker} #gray\n"
        self.relation += "\n"

        for i in range(len(parents)):
            self.make_relation(parents[i], children[i], descriptions[i])
            self.make_note(parents[i], children[i], descriptions[i])

        self.output_relation(f"{filename.split('.')[-2]}.md")
        self.output_note(f"{filename.split('.')[-2]}.md")


    def make_all_from_excel(self, filename):
        self.make_entities_from_excel(filename)
        load_file_name = filename.split(".")[-2] + ".md"
        self.make_relations_from_excel(filename, f"{load_file_name}")

    
    def output_table(self, out_name):
        out_dir = "tables"
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        with open(f"{out_dir}/{out_name}", "w") as f:
            self.obj += "@enduml"
            f.write(self.obj)


    def output_relation(self, out_name):
        out_dir = "relations"
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        with open(f"{out_dir}/relation-{out_name}", "w") as f:
            self.relation += "@enduml"
            f.write(self.relation)


    def output_note(self, out_name):
        out_dir = "notes"
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        with open(f"{out_dir}/note-{out_name}", "w") as f:
            self.note += "@enduml"
            f.write(self.note)

def build_parser():
    description="""
    ER図作成ツールです。実行のヒント:
    python ER_diagram_generator.py --generate_excel (--excel_file [path/to/file])
    python ER_diagram_generator.py --make_tables (--excel_file [path/to/file])
    python ER_diagram_generator.py --make_relations (--excel_file [path/to/file])
    python ER_diagram_generator.py --make_all (--excel_file [path/to/file])
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=description)
    parser.add_argument("-e", "--make_empty_book", action="store_true",
                        help="テーブル定義書のエクセルファイルを生成する。")
    parser.add_argument("-g", "--generate_excel", action="store_true", 
                        help="テーブル定義用のサンプル付きエクセルファイルを生成する。")
    parser.add_argument("-t", "--make_tables", action="store_true", 
                        help="テーブルの一覧を生成する。")
    parser.add_argument("-r", "--make_relations", action="store_true",
                        help="テーブルの関係を作成する。変数は表示しない。")
    parser.add_argument("-a", "--make_all", action="store_true", 
                        help="テーブルの関係を、PKとFK付きで表示する。")
    parser.add_argument("-f", "--excel_file", type=str, default="sample_format.xlsx",
                        help="入力ファイル名を指定する。デフォルトは'sample_format.xlsx'")
    parser.add_argument("-n", "--n_sheets", type=int, default=3,
                        help="テーブル数")
    return parser

def main():
    args = build_parser().parse_args()
    er = ERDiagram()
    if args.make_empty_book:
        make_excel.make_empty_book(args.excel_file, args.n_sheets)
    if args.generate_excel:
        #generate_excelbook(args.excel_file)
        make_excel.generate_excelbook(args.excel_file)
    if args.make_tables:
        er.make_entities_from_excel(args.excel_file)
    if args.make_relations:
        er.make_relations_from_excel(args.excel_file, None)
    if args.make_all:
        er.make_all_from_excel(args.excel_file)

if __name__ == "__main__":
    main()