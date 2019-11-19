#!/bin/bash

curl http://127.0.0.1:5000/cookease/recipes/ -X GET \
-d 'type=appetisers&cuisine=Indian&Ingredients=tomato&Ingredients=potato&Ingredients=chickpeas&Ingredients=salt&Ingredients=lemon&count=1'

echo "request 2"

curl http://127.0.0.1:5000/cookease/recipes/id/ -X GET \
-d 'id=20482'
