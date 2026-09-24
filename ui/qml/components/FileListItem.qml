import QtQuick
import ".."

Rectangle {
    id: root

    property var itemData: modelData
    readonly property bool isSelected: itemData ? itemData.selected : false
    readonly property string itemStatus: itemData ? itemData.status : ""

    width: parent ? parent.width : 300
    height: 48
    radius: FluentTheme.radiusSm

    color: isSelected 
           ? (FluentTheme.isDark ? "#2A3548" : "#E5F1FB")
           : (mouseArea.containsMouse ? FluentTheme.bgCardHover : "transparent")

    border.color: isSelected ? FluentTheme.accent : (mouseArea.containsMouse ? FluentTheme.borderSubtle : "transparent")
    border.width: 1

    Behavior on color {
        ColorAnimation { duration: FluentTheme.animFast }
    }

    Row {
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        spacing: 12

        // Custom Windows 11 style Checkbox
        Rectangle {
            width: 18
            height: 18
            radius: 4
            anchors.verticalCenter: parent.verticalCenter
            color: root.isSelected ? FluentTheme.accent : "transparent"
            border.color: root.isSelected ? FluentTheme.accent : FluentTheme.borderHover
            border.width: 1.5

            Image {
                visible: root.isSelected
                source: bridge.icons.check
                sourceSize.width: 12
                sourceSize.height: 12
                width: 12
                height: 12
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: bridge.toggleFileSelection(root.itemData.path)
            }
        }

        // Mini Thumbnail
        Rectangle {
            width: 36
            height: 36
            radius: 4
            color: FluentTheme.isDark ? "#1C0F13" : "#EAEAEA"
            anchors.verticalCenter: parent.verticalCenter
            clip: true

            Image {
                anchors.fill: parent
                source: root.itemData ? root.itemData.url : ""
                sourceSize.width: 72
                sourceSize.height: 72
                fillMode: Image.PreserveAspectCrop
                asynchronous: true
                cache: true
            }
        }

        // Name & Format Badge
        Row {
            anchors.verticalCenter: parent.verticalCenter
            spacing: 8
            width: parent.width - 240

            Text {
                text: root.itemData ? root.itemData.name : ""
                font.family: FluentTheme.fontFamily
                font.pixelSize: FluentTheme.fontSizeBody
                font.weight: Font.DemiBold
                color: FluentTheme.textPrimary
                elide: Text.ElideMiddle
                anchors.verticalCenter: parent.verticalCenter
                width: Math.min(implicitWidth, parent.width - 50)
            }

            Rectangle {
                height: 16
                width: fmtBadgeText.implicitWidth + 8
                radius: 3
                color: FluentTheme.isDark ? "#4E2C39" : "#D8EEFB"
                anchors.verticalCenter: parent.verticalCenter

                Text {
                    id: fmtBadgeText
                    text: root.itemData ? root.itemData.ext : ""
                    font.family: FluentTheme.fontFamily
                    font.pixelSize: 9
                    font.weight: Font.DemiBold
                    color: FluentTheme.textSecondary
                    anchors.centerIn: parent
                }
            }
        }

        // Size
        Text {
            text: root.itemData ? root.itemData.sizeFormatted : ""
            font.family: FluentTheme.fontFamily
            font.pixelSize: FluentTheme.fontSizeSmall
            color: FluentTheme.textSecondary
            anchors.verticalCenter: parent.verticalCenter
            width: 70
            horizontalAlignment: Text.AlignRight
        }

        // Status Indicator (SVG)
        Item {
            width: 24
            height: 24
            anchors.verticalCenter: parent.verticalCenter

            LoadingSpinner {
                visible: root.itemStatus === "processing"
                size: 16
                anchors.centerIn: parent
            }

            Image {
                visible: root.itemStatus === "success"
                source: bridge.icons.check
                sourceSize.width: 16
                sourceSize.height: 16
                width: 16
                height: 16
                anchors.centerIn: parent
            }

            Image {
                visible: root.itemStatus === "error"
                source: bridge.icons.error
                sourceSize.width: 16
                sourceSize.height: 16
                width: 16
                height: 16
                anchors.centerIn: parent
            }
        }

        // Delete Row Button
        Rectangle {
            width: 26
            height: 26
            radius: 4
            color: delListMouse.containsMouse ? (FluentTheme.isDark ? "#4A2020" : "#FDD") : "transparent"
            anchors.verticalCenter: parent.verticalCenter

            Image {
                source: bridge.icons.delete
                sourceSize.width: 14
                sourceSize.height: 14
                width: 14
                height: 14
                anchors.centerIn: parent
                opacity: delListMouse.containsMouse ? 1.0 : 0.6
            }

            MouseArea {
                id: delListMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: bridge.removeFile(root.itemData.path)
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        z: -1
        onClicked: bridge.toggleFileSelection(root.itemData.path)
    }
}
