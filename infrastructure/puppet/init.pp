package { 'python3':
  ensure => installed,
}

file { '/opt/incident-timeline':
  ensure => directory,
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

file { '/opt/incident-timeline/sample_logs.txt':
  ensure  => file,
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => "2026-03-19 09:00:00 INFO Service boot initiated\n2026-03-19 09:02:00 INFO Database connected\n2026-03-19 09:05:00 ERROR API gateway timeout\n2026-03-19 09:10:00 INFO Service recovery completed\n",
  require => [Package['python3'], File['/opt/incident-timeline']],
}

file { '/opt/incident-timeline/check_error_logs.py':
  ensure  => file,
  owner   => 'root',
  group   => 'root',
  mode    => '0755',
  content => "from pathlib import Path\nimport sys\n\n\ndef main():\n    log_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/opt/incident-timeline/sample_logs.txt')\n    if not log_file.exists():\n        print(f'CRITICAL: log file missing - {log_file}')\n        return 2\n    errors = [line.strip() for line in log_file.read_text(encoding='utf-8').splitlines() if ' ERROR ' in line]\n    if not errors:\n        print(f'OK: no ERROR entries found in {log_file}')\n        return 0\n    print(f'CRITICAL: {len(errors)} ERROR entries found in {log_file}')\n    for entry in errors:\n        print(entry)\n    return 2\n\n\nif __name__ == '__main__':\n    raise SystemExit(main())\n",
  require => [Package['python3'], File['/opt/incident-timeline']],
}
