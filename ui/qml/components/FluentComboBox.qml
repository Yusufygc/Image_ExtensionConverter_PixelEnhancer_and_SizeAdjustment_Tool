import QtQuick
import ".."

Rectangle {
    id: root

    signal activated(int index)

    property var model: []
    property int currentIndex: 0
    readonly property string currentText: (model && model.length > currentIndex && currentIndex >= 0) ? model[currentIndex] : ""
    property bool popupOpen: false

    implicitHeight: 36
    implicitWidth: 160
    radius: FluentTheme.radiusMd
    color: popupOpen ? FluentTheme.bgCardActive : (mouseArea.containsMouse ? FluentTheme.bgCardHover : FluentTheme.bgInput)
    border.color: popupOpen ? FluentTheme.accent : (mouseArea.containsMouse ? FluentTheme.borderHover : FluentTheme.borderSubtle)
    border.width: 1

    Behavior on border.color {
        ColorAnimation { duration: FluentTheme.animFast }
    }

    Text {
        id: currentTextLabel
        text: root.currentText
        anchors.left: parent.left
        anchors.leftMargin: 12
        anchors.right: chevron.left
        anchors.rightMargin: 8
        anchors.verticalCenter: parent.verticalCenter
        elide: Text.ElideRight
        font.family: FluentTheme.fontFamily
        font.pixelSize: FluentTheme.fontSizeBody
        color: FluentTheme.textPrimary
    }

    Canvas {
        id: chevron
        anchors.right: parent.right
        anchors.rightMargin: 12
        anchors.verticalCenter: parent.verticalCenter
        width: 12
        height: 7
        antialiasing: true
        rotation: root.popupOpen ? 180 : 0

        property color strokeColor: root.popupOpen
            ? FluentTheme.accent
            : (mouseArea.containsMouse
               ? (FluentTheme.isDark ? "#FFFFFF" : "#000000")
               : (FluentTheme.isDark ? "#E0E0E0" : "#2B2D31"))

        onStrokeColorChanged: requestPaint()

        Connections {
            target: FluentTheme
            function onIsDarkChanged() { chevron.requestPaint(); }
        }

        onPaint: {
            var ctx = getContext("2d");
            ctx.reset();
            ctx.beginPath();
            ctx.moveTo(1.5, 1.5);
            ctx.lineTo(6, 5.5);
            ctx.lineTo(10.5, 1.5);
            ctx.lineWidth = 2.2;
            ctx.strokeStyle = strokeColor;
            ctx.lineCap = "round";
            ctx.lineJoin = "round";
            ctx.stroke();
        }

        Behavior on rotation {
            NumberAnimation { duration: FluentTheme.animFast }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            root.popupOpen = !root.popupOpen
        }
    }

    // Dropdown Popup Layer
    Loader {
        id: popupLoader
        active: root.popupOpen
        sourceComponent: Component {
            Item {
                parent: root.Window.contentItem
                anchors.fill: parent
                z: 9999

                // Overlay to close popup on outside click
                MouseArea {
                    anchors.fill: parent
                    onClicked: root.popupOpen = false
                }

                Rectangle {
                    id: menuBox
                    property var rootCoords: root.mapToItem(null, 0, 0)
                    x: rootCoords.x
                    y: rootCoords.y + root.height + 4
                    width: Math.max(root.width, 180)
                    height: Math.min(itemList.contentHeight + 8, 220)
                    radius: FluentTheme.radiusMd
                    color: FluentTheme.bgSecondary
                    border.color: FluentTheme.borderHover
                    border.width: 1

                    ListView {
                        id: itemList
                        anchors.fill: parent
                        anchors.margins: 4
                        clip: true
                        model: root.model

                        delegate: Rectangle {
                            id: itemDelegate
                            width: itemList.width
                            height: 32
                            radius: FluentTheme.radiusSm
                            color: itemMouse.containsMouse 
                                   ? FluentTheme.bgCardHover 
                                   : (index === root.currentIndex ? (FluentTheme.isDark ? "#383838" : "#EBEBEB") : "transparent")

                            Text {
                                text: modelData
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.left: parent.left
                                anchors.leftMargin: 10
                                anchors.right: parent.right
                                anchors.rightMargin: 10
                                elide: Text.ElideRight
                                font.family: FluentTheme.fontFamily
                                font.pixelSize: FluentTheme.fontSizeBody
                                font.weight: index === root.currentIndex ? Font.DemiBold : Font.Normal
                                color: index === root.currentIndex ? FluentTheme.accent : FluentTheme.textPrimary
                            }

                            MouseArea {
                                id: itemMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    root.currentIndex = index
                                    root.activated(index)
                                    root.popupOpen = false
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
