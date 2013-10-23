#!/bin/sh

CLASSES=$(scripts/get-all-classes.sh )

for c in $CLASSES; do
  cat <<EOT
class $c(ModelResource):
    class Meta:
        queryset = $c.objects.all()
        allowed_methods = ['get']


EOT
done
