import lxml
import pyautogui

pyautogui.FAILSAFE = False
import xmltodict
from pynput.keyboard import Key, Controller
import time
from lxml import etree
from io import StringIO
import xml.etree.ElementTree as ET
import json
import pprint
import logging


class Custom_Controls:

    def __init__(self):
        pass


def MinimizeWindow():
    print("calls python function")

    for i in range(1, 3):
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('-')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('-')


def Upload_files(file_path: str):
    time.sleep(4)
    keyword = Controller()
    #sample file path C:\\filename
    keyword.type(file_path)
    keyword.press(Key.enter)
    keyword.release(Key.enter)
    time.sleep(3)


JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""

path = r'"C:\\Users\\10712370\\PycharmProjects\\pythonProject\\BPxPoc\\Resources\\Portal\\Keywords\\template_01.docx"'


def drag_and_drop_file(drop_target):
    driver = drop_target.parent
    file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
    file_input.send_keys(path)


#driver = webdriver.chrome(executable_path="../../../Drivers/chromedriver.exe")

#def Drag_drop_using_actionChain(drag,drop):
# actions = ActionChains(driver)
#  actions.drag_and_drop(drag,drop).perform()

def Compare_Xml_files(Actualxml, Expectedxml):
    # Actual xml convert into dictionary
    tree = ET.parse(Actualxml)
    Actualxml_data = tree.getroot()
    Actualxmlstr = ET.tostring(Actualxml_data, encoding='utf-8', method='xml')
    Actual_XML_data_dict = dict(xmltodict.parse(Actualxmlstr))

    #Expected xml convert into dictionary
    tree = ET.parse(Expectedxml)
    Expected_xml_data = tree.getroot()
    Expected_xmlstr = ET.tostring(Expected_xml_data, encoding='utf-8', method='xml')
    Expected_XML_data_dict = dict(xmltodict.parse(Expected_xmlstr))

    pprint.pprint(Actual_XML_data_dict)
    pprint.pprint(Expected_XML_data_dict)

    if len(Actual_XML_data_dict) != len(Expected_XML_data_dict):
        assert False, f"XML count doesn't match "
        #print("Not equal")
        #logging.error(f"ERROR: Output data is not as expected *****: {"Not equal"}")

    else:
        flag = 0
        for i in Actual_XML_data_dict:
            if Actual_XML_data_dict.get(i) != Expected_XML_data_dict.get(i):
                flag = 1
                assert False, f"{i} Node Not Matched "
                #break
        if flag == 0:
            print("Actual XML and Expected XML are Equal")
            logging.info(f"Exclude attributes and validate - Result = {Actual_XML_data_dict}")
        else:
            print("Not equal")
            assert False, f"{i} Node Not Matched "
            #logging.error(f"ERROR: Output data is not as expected *****: {"Not equal"}")
