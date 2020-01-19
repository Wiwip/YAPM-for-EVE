import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Item {
    GroupBox {
        id: groupBox
        x: 16
        y: 19
        width: 300
        height: 352
        title: qsTr("Origin")

        ComboBox {
            id: comboBoxOriginInstalls
            x: 99
            y: 22
            width: 177
            height: 40
        }

        ComboBox {
            id: comboBoxOriginProfiles
            x: 99
            y: 76
            width: 177
            height: 40
        }
    }

    GroupBox {
        id: groupBox1
        x: 322
        y: 19
        width: 300
        height: 352
        title: qsTr("Destination")
        ComboBox {
            id: comboBox2
            x: 99
            y: 22
            width: 177
            height: 40
        }

        ComboBox {
            id: comboBox3
            x: 99
            y: 76
            width: 177
            height: 40
        }
    }

}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
