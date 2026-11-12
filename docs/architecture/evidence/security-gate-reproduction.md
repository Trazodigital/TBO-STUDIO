# Isolated stack/security-gate reproduction

Documentation-only fixture, not product implementation or real OSV execution.
Run the following Python from the repository root with `/usr/bin/python3 -B -`.
It uses temporary directories, runs fake scanner processes against the real
framework gate, prints observations, and never changes `.framework`.

```python
"""Documentation evidence, not product tests or a real OSV-Scanner execution."""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import sys

import yaml

ROOT = Path.cwd()  # Run from the product root.
sys.path.insert(0, str(ROOT / '.framework'))
from tools.validate_contract_tool import validate
from gates.sup.scan_security_gate import check

base = {
    'contract': 'stack.v2', 'areas': [], 'code_files': ['**/*.ts'],
    'env_read_patterns': [], 'decision_record': 'docs/decisions/0001-stack.md',
}
version_cases = [
    ('Loki HTTP API', 'external_services', 'v1'),
    ('Apps Script deployment VERSION NUMBER (illustrative control, not TBO)', 'external_services', '17'),
    ('Gemini Live API', 'external_services', 'v1beta'),
    ('Vercel managed Node.js runtime', 'runtime', '24.x'),
    ('Google Sheets hosted service', 'external_services', None),
    ('Grafana Faro Cloud collector', 'external_services', None),
    ('gemini-3.8-live MODEL public version, not API version', 'llm', '3.8'),
]
versions = []
for name, area, version in version_cases:
    row = {'tool': name, 'area': area}
    if version is not None:
        row['version'] = version
    problems = validate({**base, 'areas': [row]}, 'stack')
    versions.append({'tool': name, 'version': version, 'schema_accepts': not problems,
                     'violations': [{'path': p.path, 'keyword': p.keyword} for p in problems]})

scanner_cases = [
    ('clean_exit_0', 0, 'clean'),
    ('medium_exit_1', 1, 'medium'),
    ('high_exit_1', 1, 'high'),
    ('unscored_exit_1', 1, 'unscored'),
    ('reserved_result_exit_2_clean_sarif', 2, 'clean'),
    ('operational_error_exit_127_clean_sarif', 127, 'clean'),
    ('no_packages_exit_128_clean_sarif', 128, 'clean'),
    ('exit_127_json_object_not_sarif', 127, 'object'),
    ('exit_127_missing_report', 127, 'missing'),
    ('exit_127_invalid_json', 127, 'invalid'),
]
scans = []
for name, exit_code, payload in scanner_cases:
    with TemporaryDirectory(prefix='tbo-scanner-evidence-') as tmp:
        root = Path(tmp)
        script = root / 'scanner_fixture.py'
        script.write_text('''import json,sys\nfrom pathlib import Path\nif '--version' in sys.argv:\n print('fixture-scanner 1.0.0');sys.exit(0)\ncase=sys.argv[1]\np=Path('report.sarif')\nif case=='object': p.write_text('{}')\nelif case=='invalid': p.write_text('not JSON')\nelif case!='missing':\n results=[]\n rules=[]\n if case!='clean':\n  props={} if case=='unscored' else {'security-severity':'6.9' if case=='medium' else '7.0'}\n  rules=[{'id':'fixture-rule','properties':props}]\n  results=[{'ruleId':'fixture-rule','message':{'text':'fixture finding'}}]\n p.write_text(json.dumps({'version':'2.1.0','runs':[{'tool':{'driver':{'name':'fixture-scanner','rules':rules}},'results':results}]}))\nsys.exit(int(sys.argv[2]))\n''')
        row = {
            'area': 'dependencies_scanner', 'tool': 'fixture-scanner', 'version': '1.0.0',
            'version_command': f'/usr/bin/python3 -B {script} --version',
            'run': f'/usr/bin/python3 -B {script} {payload} {exit_code}', 'results': 'report.sarif',
        }
        stack = root / 'stack.yaml'
        stack.write_text(yaml.safe_dump({**base, 'areas': [row]}))
        config = SimpleNamespace(root=root, stack_file=stack, verification_plan_file=root / 'no-plan.md',
                                 relative=lambda p: str(Path(p).relative_to(root)) if Path(p).is_absolute() else str(p))
        findings = check(config)
        scans.append({'case': name, 'fixture_exit': exit_code,
                      'rules': [f.rule for f in findings], 'gate_passes': not findings})

result = {'scope': 'schema checks and real framework security gate against synthetic scanner processes; NOT a real OSV run',
          'versions': versions, 'scanner_cases': scans}
print(json.dumps(result, indent=2))
```
