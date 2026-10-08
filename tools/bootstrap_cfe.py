# -*- coding: utf-8 -*-
from pathlib import Path
import uuid as uuidlib
import json

ext = Path(r"D:\Projects\052_AiF\src\cfe\АиФ_МСФО")
cf = Path(r"D:\Projects\052_AiF\src\cf")

cfg_xml = """<?xml version="1.0" encoding="UTF-8"?>
<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logform" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enums" xmlns:xpr="http://v8.1c.ru/8.3/xcf/predef" xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.20">
\t<Configuration uuid="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee">
\t\t<InternalInfo/>
\t\t<Properties>
\t\t\t<Name>БухгалтерияДляКазахстана</Name>
\t\t\t<Synonym><v8:item><v8:lang>ru</v8:lang><v8:content>Бухгалтерия для Казахстана</v8:content></v8:item></Synonym>
\t\t\t<DefaultLanguage>Language.Русский</DefaultLanguage>
\t\t\t<ScriptVariant>Russian</ScriptVariant>
\t\t</Properties>
\t\t<ChildObjects>
\t\t\t<Language>Русский</Language>
\t\t\t<Catalog>Организации</Catalog>
\t\t\t<Catalog>Контрагенты</Catalog>
\t\t\t<ChartOfAccounts>Типовой</ChartOfAccounts>
\t\t</ChildObjects>
\t</Configuration>
</MetaDataObject>
"""
(cf / "Configuration.xml").write_text(cfg_xml, encoding="utf-8")
print("cf Configuration.xml written")


def make_adopted(folder: str, name: str, tag: str, base_uuid: str) -> None:
    new_uuid = str(uuidlib.uuid4())

    def gt(gen_name: str, category: str) -> str:
        return (
            f'\t\t\t<xr:GeneratedType name="{gen_name}" category="{category}">\n'
            f"\t\t\t\t<xr:TypeId>{uuidlib.uuid4()}</xr:TypeId>\n"
            f"\t\t\t\t<xr:ValueId>{uuidlib.uuid4()}</xr:ValueId>\n"
            f"\t\t\t</xr:GeneratedType>"
        )

    gens = "\n".join(
        [
            gt(f"{tag}Object.{name}", "Object"),
            gt(f"{tag}Ref.{name}", "Ref"),
            gt(f"{tag}Selection.{name}", "Selection"),
            gt(f"{tag}List.{name}", "List"),
            gt(f"{tag}Manager.{name}", "Manager"),
        ]
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logform" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enums" xmlns:xpr="http://v8.1c.ru/8.3/xcf/predef" xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.20">
\t<{tag} uuid="{new_uuid}">
\t\t<InternalInfo>
{gens}
\t\t</InternalInfo>
\t\t<Properties>
\t\t\t<ObjectBelonging>Adopted</ObjectBelonging>
\t\t\t<Name>{name}</Name>
\t\t\t<Comment/>
\t\t\t<ExtendedConfigurationObject>{base_uuid}</ExtendedConfigurationObject>
\t\t</Properties>
\t\t<ChildObjects/>
\t</{tag}>
</MetaDataObject>
"""
    out_dir = ext / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{name}.xml").write_text(xml, encoding="utf-8")
    print("adopted", name)


make_adopted("Catalogs", "Организации", "Catalog", "382bbe17-739e-4149-b15b-d5ac11829f24")
make_adopted("Catalogs", "Контрагенты", "Catalog", "85a292c7-1c29-4647-ae4b-5eff279641e9")

cfg_path = ext / "Configuration.xml"
text = cfg_path.read_text(encoding="utf-8")
if "<Catalog>Организации</Catalog>" not in text:
    text = text.replace(
        "</ChildObjects>",
        "\t\t\t<Catalog>Организации</Catalog>\n"
        "\t\t\t<Catalog>Контрагенты</Catalog>\n"
        "\t\t</ChildObjects>",
    )
    cfg_path.write_text(text, encoding="utf-8")
    print("Configuration.xml updated")
else:
    print("already registered")

# Write meta-compile JSON batch
meta = [
    {
        "type": "Enum",
        "name": "АиФ_ВидыОперацийМСФО",
        "synonym": "Виды операций МСФО (АиФ)",
        "values": [
            "Переклассификация",
            "ПереносМеждуЮЛ",
            "ИсключениеВГО",
            "Прочее",
        ],
    },
    {
        "type": "Catalog",
        "name": "АиФ_СтатьиМСФО",
        "synonym": "Статьи МСФО (АиФ)",
        "descriptionLength": 150,
        "codeLength": 20,
        "attributes": [
            "КодМСФО: String(20)",
            "ЭтоРасходПериода: Boolean",
            "Комментарий: String(200) | multiline",
        ],
    },
    {
        "type": "Catalog",
        "name": "АиФ_ПериметрГруппы",
        "synonym": "Периметр группы (АиФ)",
        "descriptionLength": 150,
        "codeLength": 9,
        "attributes": [
            "Организация: CatalogRef.Организации | req",
            "ВходитВКонсолидацию: Boolean",
            "ИсключатьВГО: Boolean",
            "Порядок: Number(5,0)",
            "Комментарий: String(200) | multiline",
        ],
    },
    {
        "type": "Catalog",
        "name": "АиФ_КартаСчетовМСФО",
        "synonym": "Карта счетов МСФО (АиФ)",
        "descriptionLength": 150,
        "codeLength": 9,
        "attributes": [
            "КодСчетаБП: String(20) | req",
            "СтатьяМСФО: CatalogRef.АиФ_СтатьиМСФО",
            "ВидОперации: EnumRef.АиФ_ВидыОперацийМСФО",
            "ПереклассифицироватьВРасходПериода: Boolean",
            "Активно: Boolean",
            "Комментарий: String(200) | multiline",
        ],
    },
    {
        "type": "Catalog",
        "name": "АиФ_ПравилаВГО",
        "synonym": "Правила исключения ВГО (АиФ)",
        "descriptionLength": 150,
        "codeLength": 9,
        "attributes": [
            "ОрганизацияПродавец: CatalogRef.Организации | req",
            "ОрганизацияПокупатель: CatalogRef.Организации | req",
            "КонтрагентПродавец: CatalogRef.Контрагенты",
            "КонтрагентПокупатель: CatalogRef.Контрагенты",
            "КодСчетаВыручки: String(20)",
            "КодСчетаЗатрат: String(20)",
            "Активно: Boolean",
            "Комментарий: String(200) | multiline",
        ],
    },
    {
        "type": "InformationRegister",
        "name": "АиФ_ДвиженияМСФО",
        "synonym": "Движения МСФО (АиФ)",
        "writeMode": "RecorderSubordinate",
        "periodicity": "RecorderPosition",
        "dimensions": [
            "Организация: CatalogRef.Организации | master, mainFilter, denyIncomplete",
            "СтатьяМСФО: CatalogRef.АиФ_СтатьиМСФО | mainFilter",
            "ВидОперации: EnumRef.АиФ_ВидыОперацийМСФО | mainFilter",
            "КодСчетаБП: String(20)",
            "Контрагент: CatalogRef.Контрагенты",
        ],
        "resources": [
            "Сумма: Number(15,2)",
            "СуммаВГО: Number(15,2)",
        ],
        "attributes": [
            "Содержание: String(200)",
            "ОбъектАналитики: String(100)",
        ],
    },
    {
        "type": "Document",
        "name": "АиФ_КорректировкаМСФО",
        "synonym": "Корректировка МСФО (АиФ)",
        "posting": "Allow",
        "registerRecords": ["InformationRegister.АиФ_ДвиженияМСФО"],
        "attributes": [
            "Организация: CatalogRef.Организации | req",
            "ВидОперации: EnumRef.АиФ_ВидыОперацийМСФО | req",
            "ПериодОтчёта: Date",
            "Комментарий: String(200) | multiline",
        ],
        "tabularSections": {
            "Строки": [
                "КодСчетаБП: String(20)",
                "СтатьяМСФО: CatalogRef.АиФ_СтатьиМСФО",
                "Контрагент: CatalogRef.Контрагенты",
                "Сумма: Number(15,2)",
                "СуммаВГО: Number(15,2)",
                "ОбъектАналитики: String(100)",
                "Содержание: String(200)",
            ]
        },
    },
    {
        "type": "CommonModule",
        "name": "АиФ_МСФОСервер",
        "synonym": "МСФО сервер (АиФ)",
        "server": True,
        "clientOrdinaryApplication": False,
        "clientManagedApplication": False,
        "externalConnection": True,
        "serverCall": True,
    },
    {
        "type": "DataProcessor",
        "name": "АиФ_ПомощникКонсолидации",
        "synonym": "Помощник консолидации МСФО (АиФ)",
        "attributes": [
            "ПериодС: Date",
            "ПериодПо: Date",
            "ТолькоАктивныеПравила: Boolean",
        ],
    },
]

out = Path(r"D:\Projects\052_AiF\tools\meta_batch.json")
out.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print("meta_batch.json written", len(meta), "objects")
