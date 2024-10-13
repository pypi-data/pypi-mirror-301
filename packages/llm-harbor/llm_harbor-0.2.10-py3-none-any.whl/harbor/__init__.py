import subprocess
import sys

def main():
  result = subprocess.run(
    ["bash", "../harbor.sh"] + sys.argv[1:],
    shell=False,
    text=True,
    check=False,
    stdout=sys.stdout,
    stderr=sys.stderr
  )
  sys.exit(result.returncode)

if __name__ == "__main__":
  main()
