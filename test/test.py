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

def testExistence():
    test_data = {
        "name" : "Bob",
        "age" : 32
    }
    keysList = list(test_data.keys())
    print(keysList)
    try:
        test_data["name"]
    except NameError:
        print('Name does not exist')
    else:
        print('Name exists')
        print(test_data["name"])
    try:
        test_data["age"]
    except NameError:
        print('age does not exist')
    else:
        print('age exists')
        print(test_data["age"])
    try:
        test_data["foobar"]
    except NameError:
        print('foobar does not exist')
    else:
        print('foobar exists')
        print(test_data["foobar"])

def testStringToColor(colorString):
    print("colorString = " + colorString)
    temp = colorString.strip("()")
    print("temp  = " + temp)
    strArray = temp.split(',')
    print("strArray =")

    r = float(strArray[0])
    g = float(strArray[1])
    b = float(strArray[2])
    color = (r, g, b)
    # color[0] = float(strArray[0])
    # color[1] = float(strArray[1])
    # color[2] = float(strArray[2])
    print("final color")
    print(color)
    return color

# testColor()
# testJSONWrite()
# testJSONRead()
# compareJSON()
# testExistence()
testStringToColor("(0.1, 0.2, 0.3)")