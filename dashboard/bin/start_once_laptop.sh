#!/bin/sh

set -eo pipefail

source "$(dirname $0)/common.sh"
eog $(dirname $0)/../svg/tmp.svg
