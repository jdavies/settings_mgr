import json

data = {
        "name" : {
            "first" : "First",
            "second" : "Second",
        },
        "age" : 32,
        "test" : "This is a test",
        "render_props": {
            "engine" : "cycles"
        }
    }

read_data = {}

def testColor():
    color = (1,2,3)
    print(color)
    print(color[1])

def testJSONWrite():
    print('Saving a JSON file')

    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=True, ensure_ascii=True, indent=4)
        f.close()
    print('JSON written:')
    print(data)

def testJSONRead():
    print('Reading in the JSON file...')
    f = open('test.json', 'r')
    read_data = json.load(f)
    f.close()
    print('JSON Read')
    print(read_data)

def compareJSON():
    if(data == read_data):
        print('Dictioaries are identical!')
    else:
        print('dictionaries are different!')

testColor()
testJSONWrite()
testJSONRead()
compareJSON()