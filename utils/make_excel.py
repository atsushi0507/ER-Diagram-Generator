from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation

def make_sheet(wb):
    ws = wb.active
    ws.title="table_1"
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 10
    ws.column_dimensions["D"].width = 35

    ws.cell(1, 1, value="Column Name")
    ws.cell(1, 2, value="Primary Key")
    ws.cell(1, 3, value="Foreign Key")
    ws.cell(1, 4, value="Comment")

    return ws

def make_table(title):
    table = Table(displayName=title, ref=f"A1:D2")
    style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    table.tableStyleInfo = style
    return table

def make_empty_book(filename="sample_format.xlsx", n_tables=4):
    wb = Workbook()
    ws = make_sheet(wb)
    ws.add_table(make_table("table_1"))
    for n in range(2, n_tables+1):
        ws = wb.copy_worksheet(wb["table_1"])
        ws.title = f"table_{n}"
        table = make_table(f"table_{n}")
        ws.add_table(table)

    ws_relation = wb.create_sheet(title="relation")
    ws_relation.column_dimensions["A"].width = 30
    ws_relation.column_dimensions["B"].width = 30

    ws_relation.cell(1, 1, value="Parent")
    ws_relation.cell(1, 2, value="Child")

    table2 = Table(displayName="Relation", ref="A1:B6")
    style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    table2.tableStyleInfo = style

    ws_relation.add_table(table2)

    ws_process = wb.create_sheet(title="process")
    ws_process.column_dimensions["A"].width = 12
    ws_process.column_dimensions["B"].width = 20
    ws_process.column_dimensions["C"].width = 25
    ws_process.column_dimensions["D"].width = 20
    ws_process.column_dimensions["E"].width = 10
    ws_process.column_dimensions["F"].width = 35

    ws_process.cell(1, 1, value="Process")
    ws_process.cell(1, 2, value="Input")
    ws_process.cell(1, 3, value="Add")
    ws_process.cell(1, 4, value="Output")
    ws_process.cell(1, 5, value="Middle Table?")
    ws_process.cell(1, 6, value="Comment")

    table3 = Table(displayName="Process", ref="A1:F2")
    table3.tableStyleInfo = style
    ws_process.add_table(table3)
    
    dv = DataValidation(
        type="list",
        formula1='"left,right,top,bottom"',
        allow_blank=True,
        showErrorMessage=True,
        errorStyle="warning",
        errorTitle="選択リストから選択してください"
    )
    dv.add(f"A2:A1000")
    ws_process.add_data_validation(dv)
    
    wb.save(filename)
    wb.close()
    print(f"Generated empty excel book: {filename}")


def make_excel_sheet(ws, title, n_column, columns, PKs, FKs, comments):
    ws.cell(1, 1, value="Column Name")
    ws.cell(1, 2, value="Primary Key")
    ws.cell(1, 3, value="Foreign Key")
    ws.cell(1, 4, value="Comment")
    for i in range(n_column):
        ws.cell(i+2, 1, value=columns[i])
        ws.cell(i+2, 2, value=PKs[i])
        ws.cell(i+2, 3, value=FKs[i])
        ws.cell(i+2, 4, value=comments[i])
    table = Table(displayName=title, ref=f"A1:D{n_column+1}")
    style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    table.tableStyleInfo = style
    return table

def generate_excelbook(filename="sample_format.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "sample_table"
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 10
    ws.column_dimensions["D"].width = 35

    columns = [f"column_{i}" for i in range(10)]
    PKs = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
    FKs = [0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
    comments = ["", "Table2の外部キー", "", "Table5の外部キー", "", "", "", "", "", ""]

    table = make_excel_sheet(ws, "Table1", len(columns), columns, PKs, FKs, comments)
    ws.add_table(table)

    ws_child1 = wb.create_sheet(title="child1")
    ws_child1.column_dimensions["A"].width = 30
    ws_child1.column_dimensions["B"].width = 10
    ws_child1.column_dimensions["C"].width = 10
    ws_child1.column_dimensions["D"].width = 35
    columns = [f"column_{i}" for i in range(7)]
    PKs = [0, 1, 0, 0, 0, 0, 0]
    FKs = [0, 0, 0, 1, 0, 0, 0]
    comments = ["" for _ in range(7)]
    table_child1 = make_excel_sheet(ws_child1, "Child1", len(columns), columns, PKs, FKs, comments)
    ws_child1.add_table(table_child1)

    ws_child2 = wb.create_sheet(title="child2")
    ws_child2.column_dimensions["A"].width = 30
    ws_child2.column_dimensions["B"].width = 10
    ws_child2.column_dimensions["C"].width = 10
    ws_child2.column_dimensions["D"].width = 35
    columns = [f"column_{i}" for i in range(4)]
    PKs = [1, 1, 0, 0]
    FKs = [0, 0, 0, 1]
    comments = ["" for _ in range(4)]
    table_child2 = make_excel_sheet(ws_child2, "Child2", len(columns), columns, PKs, FKs, comments)
    ws_child2.add_table(table_child2)

    ws_child3 = wb.create_sheet(title="child3")
    ws_child3.column_dimensions["A"].width = 30
    ws_child3.column_dimensions["B"].width = 10
    ws_child3.column_dimensions["C"].width = 10
    ws_child3.column_dimensions["D"].width = 35
    columns = [f"column_{i}" for i in range(6)]
    PKs = [1, 0, 0, 0, 0, 0]
    FKs = [0, 0, 0, 0, 1, 0]
    comments = ["" for _ in range(6)]
    table_child3 = make_excel_sheet(ws_child3, "Child3", len(columns), columns, PKs, FKs, comments)
    ws_child3.add_table(table_child3)

    ws_child4 = wb.create_sheet(title="child4")
    ws_child4.column_dimensions["A"].width = 30
    ws_child4.column_dimensions["B"].width = 10
    ws_child4.column_dimensions["C"].width = 10
    ws_child4.column_dimensions["D"].width = 35
    columns = [f"column_{i}" for i in range(5)]
    PKs = [1, 1, 0, 1, 0]
    FKs = [0, 0, 0, 1, 0]
    comments = ["" for _ in range(5)]
    table_child4 = make_excel_sheet(ws_child4, "Child4", len(columns), columns, PKs, FKs, comments)
    ws_child4.add_table(table_child4)

    ws_child5 = wb.create_sheet(title="child5")
    ws_child5.column_dimensions["A"].width = 30
    ws_child5.column_dimensions["B"].width = 10
    ws_child5.column_dimensions["C"].width = 10
    ws_child5.column_dimensions["D"].width = 35
    columns = [f"column_{i}" for i in range(4)]
    PKs = [1, 1, 0, 0]
    FKs = [0, 0, 0, 1]
    comments = ["" for _ in range(4)]
    table_child5 = make_excel_sheet(ws_child5, "Child5", len(columns), columns, PKs, FKs, comments)
    ws_child5.add_table(table_child5)

    ws_relation = wb.create_sheet(title="relation")
    ws_relation.column_dimensions["A"].width = 30
    ws_relation.column_dimensions["B"].width = 30
    relations = {
        # parent : child
        "sample_table" : ["child1", "child2", "child3"],
        "child1" : ["child4"],
        "child2" : ["child5"]
    }
    ws_relation.cell(1, 1, value="Parent")
    ws_relation.cell(1, 2, value="Child")
    i = 2
    for key, val in relations.items():
        for v in val:
            ws_relation.cell(i, 1, value=key)
            ws_relation.cell(i, 2, value=v)
            i += 1

    table2 = Table(displayName="Relation", ref="A1:B6")
    style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
    table2.tableStyleInfo = style

    ws_relation.add_table(table2)

    ws_process = wb.create_sheet(title="process")
    ws_process.column_dimensions["A"].width = 12
    ws_process.column_dimensions["B"].width = 20
    ws_process.column_dimensions["C"].width = 25
    ws_process.column_dimensions["D"].width = 20
    ws_process.column_dimensions["E"].width = 10
    ws_process.column_dimensions["F"].width = 35

    ws_process.cell(1, 1, value="Process")
    ws_process.cell(1, 2, value="Input")
    ws_process.cell(1, 3, value="Add")
    ws_process.cell(1, 4, value="Output")
    ws_process.cell(1, 5, value="Middle Table?")
    ws_process.cell(1, 6, value="Comment")

    table3 = Table(displayName="Process", ref="A1:F2")
    table3.tableStyleInfo = style
    ws_process.add_table(table3)

    processes = [
        ["", "s456", "pboem", "join1", None, ""],
        ["", "join1", "deadline", "join2", None, ""],
        ["", "join2", "MD_price", "join3", None, ""],
        ["", "join3", "", "self.s456", 1, None, ""],
        ["", "self.s456", "self.psku", "join4", None, ""],
    ]
    for i, process in enumerate(processes):
        for j, val in enumerate(process):
            if (j == 0 and val == 0):
                ws_process.cell(i+2, j+1, value="")
            else:
                 ws_process.cell(i+2, j+1, value=val)

    dv = DataValidation(
        type="list",
        formula1='"join,union,process,make_middle_table"',
        allow_blank=True,
        showErrorMessage=True,
        errorStyle="warning",
        errorTitle="選択リストから選択してください"
    )
    dv.add(f"A2:A1000")
    ws_process.add_data_validation(dv)


    wb.save(filename)
    print(f"Generated {filename}")