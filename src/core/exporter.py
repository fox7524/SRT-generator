import xml.etree.ElementTree as ET
import xml.dom.minidom

def format_timestamp_srt(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def export_srt(segments: list, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp_srt(segment['start'])
            end = format_timestamp_srt(segment['end'])
            text = segment['text'].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

def export_txt(segments: list, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(f"{segment['text'].strip()}\n")

def export_rtf(segments: list, output_path: str):
    # Basit RTF yapısı
    header = r"{\rtf1\ansi\ansicpg1252\deff0\nouicompat{\fonttbl{\f0\fnil\fcharset0 Calibri;}}" + "\n"
    content = ""
    for segment in segments:
        text = segment['text'].strip().replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')
        content += rf"{text}\par" + "\n"
    footer = "}"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + content + footer)

def export_xml(segments: list, output_path: str):
    root = ET.Element("transcript")
    for i, segment in enumerate(segments, start=1):
        seg_elem = ET.SubElement(root, "segment", id=str(i))
        start_elem = ET.SubElement(seg_elem, "start")
        start_elem.text = str(segment['start'])
        end_elem = ET.SubElement(seg_elem, "end")
        end_elem.text = str(segment['end'])
        text_elem = ET.SubElement(seg_elem, "text")
        text_elem.text = segment['text'].strip()
        
    xml_str = ET.tostring(root, encoding="utf-8")
    parsed_xml = xml.dom.minidom.parseString(xml_str)
    pretty_xml = parsed_xml.toprettyxml(indent="  ")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
