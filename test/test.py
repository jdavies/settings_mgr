import json


def testColor():
    color = (1,2,3)
    print(color)
    print(color[1])

def testJSON():
    print('Saving a JSON file')

    data = {
        "name" : {
            "first" : "First",
            "second" : "Second",
        },
        "age" : 32
    }

    # Create a new root level attribute
    data['test'] = 'This is a test'
    # Create a new object section
    data['render_props'] = {}
    # Add an attibute to the new section.
    data['render_props']['engine'] = 'cycles'

    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=True, ensure_ascii=True, indent=4)

testColor()