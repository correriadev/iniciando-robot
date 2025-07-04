# extract_robot_data.py
import xml.etree.ElementTree as ET
import json
import argparse

def extract_robot_framework_results(input_path, output_path):
    results = []
    tree = ET.parse(input_path)
    root = tree.getroot()

    for test in root.iter('test'):
        name = test.attrib.get('name')
        status_elem = test.find('status')
        status = status_elem.attrib.get('status') if status_elem is not None else 'UNKNOWN'

        error_msg = None
        for kw in test.iter('kw'):
            kw_status = kw.find('status')
            if kw_status is not None and kw_status.attrib.get('status') == 'FAIL':
                error_msg = kw_status.text.strip() if kw_status.text else 'Erro desconhecido'
                break

        result = {'name': name, 'status': status}
        if status == 'FAIL' and error_msg:
            result['error'] = error_msg

        results.append(result)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    extract_robot_framework_results(args.input, args.output)


# extract_postman_data.py
import json
import argparse

def extract_postman_results(input_path, output_path):
    with open(input_path) as f:
        data = json.load(f)

    results = []
    for execution in data.get('executions', []):
        name = execution.get('item', {}).get('name', 'Unknown')
        assertions = execution.get('assertions', [])

        failed_assertions = [a for a in assertions if not a.get('passed', True)]
        status = 'FAIL' if failed_assertions else 'PASS'
        error_msg = failed_assertions[0].get('error', 'Erro desconhecido') if failed_assertions else None

        result = {'name': name, 'status': status}
        if status == 'FAIL' and error_msg:
            result['error'] = error_msg

        results.append(result)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    extract_postman_results(args.input, args.output)


# analyze_results.py
import json
import argparse

def analyze_results(robot_path, postman_path, output_path):
    with open(robot_path) as f:
        robot_results = json.load(f)
    with open(postman_path) as f:
        postman_results = json.load(f)

    all_results = robot_results + postman_results

    total = len(all_results)
    passed = sum(1 for r in all_results if r['status'] == 'PASS')
    failed = sum(1 for r in all_results if r['status'] == 'FAIL')

    failed_details = [r for r in all_results if r['status'] == 'FAIL']

    summary = {
        'total_tests': total,
        'passed_tests': passed,
        'failed_tests': failed,
        'failed_details': failed_details
    }

    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--robot', required=True)
    parser.add_argument('--postman', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    analyze_results(args.robot, args.postman, args.output)


# publish_to_confluence.py
import json
import argparse
import os
from atlassian import Confluence
from datetime import datetime

def publish_report(input_path):
    url = os.environ['CONFLUENCE_URL']
    username = os.environ['CONFLUENCE_USERNAME']
    api_token = os.environ['CONFLUENCE_API_TOKEN']
    space_key = os.environ['SPACE_KEY']
    parent_id = os.environ['PARENT_PAGE_ID']

    with open(input_path) as f:
        summary = json.load(f)

    title = f"Relatório de Testes - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    content = f"""
<h1>{title}</h1>
<p><strong>Total de Testes:</strong> {summary['total_tests']}</p>
<p><strong>Passaram:</strong> {summary['passed_tests']}</p>
<p><strong>Falharam:</strong> {summary['failed_tests']}</p>
<h2>Detalhes das Falhas:</h2>
<table>
<tr><th>Nome</th><th>Erro</th></tr>
"""
    for fail in summary['failed_details']:
        content += f"<tr><td>{fail['name']}</td><td>{fail.get('error', 'Erro não informado')}</td></tr>"

    content += "</table>"

    confluence = Confluence(
        url=url,
        username=username,
        password=api_token
    )

    confluence.create_page(space=space_key, title=title, body=content, parent_id=parent_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    publish_report(args.input)


# main.py
import subprocess
import os

def main():
    print("📝 Extraindo resultados do Robot Framework...")
    subprocess.run(["python", "extract_robot_data.py", "--input", "./resultados/output.xml", "--output", "robot_data.json"], check=True)

    print("📝 Extraindo resultados do Postman (Newman)...")
    subprocess.run(["python", "extract_postman_data.py", "--input", "./resultados/postman_report.json", "--output", "postman_data.json"], check=True)

    print("🔍 Consolidando e analisando os resultados...")
    subprocess.run(["python", "analyze_results.py", "--robot", "robot_data.json", "--postman", "postman_data.json", "--output", "resumo.json"], check=True)

    print("📢 Publicando relatório no Confluence...")
    subprocess.run(["python", "publish_to_confluence.py", "--input", "resumo.json"], check=True)

    print("✅ Processo concluído com sucesso!")

if __name__ == "__main__":
    main()


# requirements.txt
beautifulsoup4
lxml
requests
atlassian-python-api
