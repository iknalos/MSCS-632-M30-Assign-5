#!/usr/bin/env bash
# Rebuilds both versions, saves their output in output/, and checks that the
# two programs print the same text apart from the first line (the language).
set -euo pipefail
cd "$(dirname "$0")/.."

make -s -C cpp
(cd cpp && ./ride_sharing) > output/cpp_output.txt
smalltalk/run.sh > output/smalltalk_output.txt

{
    echo "\$ diff <(tail -n +2 output/cpp_output.txt) <(tail -n +2 output/smalltalk_output.txt)"
    if diff <(tail -n +2 output/cpp_output.txt) <(tail -n +2 output/smalltalk_output.txt); then
        echo "identical: $(($(wc -l < output/cpp_output.txt) - 1)) lines after the header match"
    else
        echo "DIFFERENT"
    fi
} > output/compare.txt
cat output/compare.txt
grep -q '^identical' output/compare.txt
