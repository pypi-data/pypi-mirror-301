#%%
import os
import argparse
from pathlib import Path
import pandas as pd
from docxtpl import DocxTemplate




def datapath(path:str):
    _ROOT = Path(__file__).parent
    return os.path.join(_ROOT,'data',path)

def name(context):
    first_part = context['p6'].replace('(','').replace(')','')
    gov = context['p2'].split('بولاية')[1] 
    second_part = 'بولاية' + gov
    ministry ='وزارة' + context['p2'].split('لوزارة')[1].split('بولاية')[0]
    date = context['p1'].replace('تونس في','').replace('/','-').strip()
    return f'{first_part.strip()} {second_part.strip()} .docx' , ministry.strip() , gov.strip(),date


def to_excel_data(context):
    gov = context['p2'].split('بولاية')[1]
    date = context['p1'].replace('تونس في','').replace('/','-').strip()
    first_part = context['p6'].replace('(','').replace(')','')
    second_part = 'بولاية' + gov
    structure = f'{first_part.strip()} {second_part.strip()}'
    information = context['p12']
    instance = context['p13']

    return {'structure' : structure.strip() ,'gov' : gov , 'instance' : instance.strip() , 'information' : information , 'date' : date }



def generate_doc(template='data/template.docx',path='data/src.csv',out='out'):
    data = pd.read_csv(path,encoding='cp1256',header=None)

    l_context = []
    for l in range(len(data)):

        item = data.iloc[l]

        context = {}
        for i,x in enumerate(item):
            if(i == 3):
                context["p" + str(i+1)] = 'رئاسة الحكومة'
            else:
                context["p" + str(i+1)] = x
        l_context.append(context)


    for i,c in enumerate(l_context):
        doc = DocxTemplate(template)
        doc.render(context=c,autoescape=True)
        n,ministry,gov,date = name(c)
        pathdir = os.path.join(out,date,ministry,gov)
        if not os.path.exists(pathdir):
            os.makedirs(pathdir)
        doc.save(os.path.join(pathdir,f'{i}-{n}') )


def generate_excel(path='data/src.csv',out='data/out.xlsx'):
    data = pd.read_csv(path,encoding='cp1256',header=None)

    columns = ['المؤسسة أو الهيكل','الولاية','المصلحة','الملاحظات','التاريخ']

    l_context = []
    for l in range(len(data)):

        item = data.iloc[l]

        context = {}
        for i,x in enumerate(item):
            context["p" + str(i+1)] = x

        l_context.append(context)
    re = {}
    for d in l_context:
        d = to_excel_data(d)
        re.setdefault(d['gov'],[]).append(d)

    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        
        for key in re.keys():
            data = pd.DataFrame(re[key])
            data.columns = columns
            data.to_excel(writer,key,index=False, startcol=1,startrow=2)

            worksheet = writer.sheets[key]
            worksheet.right_to_left()



def cli():
    parser = argparse.ArgumentParser(
        prog ="export data to word document",
        description="Arguments for expreport",
        usage = "",
        allow_abbrev=True
    )

    parser.add_argument(
        "--data",
        type=str,
        help="path of source data"
    )

    parser.add_argument(
        "--template",
        type=str,
        help="path of template to generate document",
        default=datapath("template.docx")
    )

    parser.add_argument(
        "--out",
        type=str,
        help="path of exported document",
        default=""
    )


    parser.add_argument(
        "--excel",
        type=bool,
        help="export excel file",
        default=False
    )

    args = parser.parse_args()


    if not os.path.exists(args.data):
        raise TypeError('File source not found please check your params --data')
    
    if not os.path.exists(args.out):
        raise TypeError('Folder to export document not found please check your params --out')
    
    if not os.path.exists(args.template):
        raise TypeError('Template file not exist please check your params --template or dont use it at all')
    
    if args.excel:
        generate_excel(args.data,os.path.join(args.out,'out.xlsx'))
    else:
        generate_doc(args.template,args.data,args.out)






# %%
