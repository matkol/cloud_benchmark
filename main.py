#!/usr/bin/env python

from app.tasks import add
import os

result = add.delay(66, 4)

print(os.getcwd())
print(result.id)
