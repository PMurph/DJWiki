# DJWiki Web Application

## Dependencies
* Django
* Lettuce

### Installation
```
pip install django
pip install lettuce
```

## Instructions

### Tests
#### Unit Tests
```
python manage.py test pages
```

#### Acceptance Tests
```
python manage.py harvest
```

#### JavaScript Tests
Note: 
* Must have the standalone test runner installed in the */resources/js directory.
* Must have chrome in PATH enviroment variable
```
chrome resources/pages/js/SpecRunner.html
```
