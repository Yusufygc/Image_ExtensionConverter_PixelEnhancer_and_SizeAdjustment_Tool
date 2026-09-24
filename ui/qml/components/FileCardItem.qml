import QtQuick
import ".."

Rectangle {
    id: root

    property var itemData: modelData
    readonly property bool isSelected: itemData ? itemData.selected : false
    readonly property string itemStatus: itemData ? itemData.status : ""

    width: 140
    height: 160
    radius: FluentTheme.radiusMd

    color: isSelected 
           ? (FluentTheme.isDark ? "#2D3E50" : "#E5F1FB")
           : (mouseArea.containsMouse ? FluentTheme.bgCardHover : FluentTheme.bgCard)

    border.color: isSelected 
                 ? FluentTheme.accent 
                 : (mouseArea.containsMouse ? FluentTheme.borderHover : FluentTheme.borderCard)
    border.width: isSelected ? 2 : 1

    Behavior on color {
        ColorAnimation { duration: FluentTheme.animFast }
    }
    Behavior on border.color {
        ColorAnimation { duration: FluentTheme.animFast }
    }

    Column {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 6

        // Thumbnail Preview Container
        Rectangle {
            width: parent.width
            height: 90
            radius: FluentTheme.radiusSm
            color: FluentTheme.isDark ? "#1C1C1C" : "#EEEEEE"
            clip: true

            Image {
                id: thumb
                anchors.fill: parent
                source: root.itemData ? root.itemData.url : ""
                sourceSize.width: 160
                sourceSize.height: 160
                fillMode: Image.PreserveAspectFit
                asynchronous: true
                cache: true

                // Fallback icon if loading fails or invalid
                onStatusChanged: {
                    if (status === Image.Error) {
                        fallbackIcon.visible = true;
                    }
                }
            }

            Image {
                id: fallbackIcon
                visible: thumb.status === Image.Error || thumb.status === Image.Null
                source: bridge.icons.file
                sourceSize.width: 32
                sourceSize.height: 32
                width: 32
                height: 32
                anchors.centerIn: parent
                opacity: 0.5
            }

            // Format Badge (Top-left of thumbnail)
            Rectangle {
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.margins: 4
                height: 16
                width: fmtText.implicitWidth + 8
                radius: 3
                color: Qt.rgba(0, 0, 0, 0.6)

                Text {
                    id: fmtText
                    text: root.itemData ? root.itemData.ext : ""
                    color: "#FFFFFF"
                    font.family: FluentTheme.fontFamily
                    font.pixelSize: 9
                    font.weight: Font.Bold
                    anchors.centerIn: parent
                }
            }

            // Status Badge (Top-right of thumbnail)
            Rectangle {
                visible: root.itemStatus !== ""
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.margins: 4
                width: 20
                height: 20
                radius: 10
                color: {
                    if (root.itemStatus === "success") return FluentTheme.successBg
                    if (root.itemStatus === "error") return FluentTheme.dangerBg
                    return Qt.rgba(0, 0, 0, 0.6)
                }

                LoadingSpinner {
                    visible: root.itemStatus === "processing"
                    size: 14
                    anchors.centerIn: parent
                }

                Image {
                    visible: root.itemStatus === "success"
                    source: bridge.icons.check
                    sourceSize.width: 13
                    sourceSize.height: 13
                    width: 13
                    height: 13
                    anchors.centerIn: parent
                }

                Image {
                    visible: root.itemStatus === "error"
                    source: bridge.icons.error
                    sourceSize.width: 13
                    sourceSize.height: 13
                    width: 13
                    height: 13
                    anchors.centerIn: parent
                }
            }
        }

        // File Details
        Text {
            width: parent.width
            text: root.itemData ? root.itemData.name : ""
            font.family: FluentTheme.fontFamily
            font.pixelSize: FluentTheme.fontSizeSmall
            font.weight: Font.DemiBold
            color: FluentTheme.textPrimary
            elide: Text.ElideMiddle
        }

        Item {
            width: parent.width
            height: 20

            Text {
                text: root.itemData ? root.itemData.sizeFormatted : ""
                font.family: FluentTheme.fontFamily
                font.pixelSize: 10
                color: FluentTheme.textSecondary
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
            }

            // Delete item button
            Rectangle {
                width: 20
                height: 20
                radius: 4
                color: delMouse.containsMouse ? (FluentTheme.isDark ? "#4A2020" : "#FDD") : "transparent"
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter

                Image {
                    source: bridge.icons.delete
                    sourceSize.width: 12
                    sourceSize.height: 12
                    width: 12
                    height: 12
                    anchors.centerIn: parent
                    opacity: delMouse.containsMouse ? 1.0 : 0.6
                }

                MouseArea {
                    id: delMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        bridge.removeFile(root.itemData.path);
                    }
                }
            }
        }
    }

    // Click area for card selection toggle
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: (mouse) => {
            // If clicked near delete button, delegate handled it
            bridge.toggleFileSelection(root.itemData.path);
        }
    }
}
