import QtQuick
import ".."
import "../components"

Item {
    id: root

    property bool isOpen: false

    visible: opacity > 0
    opacity: isOpen ? 1.0 : 0.0

    Behavior on opacity {
        NumberAnimation { duration: FluentTheme.animNormal; easing.type: Easing.OutCubic }
    }

    // Backdrop shadow/tint
    Rectangle {
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, 0.45)

        MouseArea {
            anchors.fill: parent
            onClicked: root.isOpen = false
        }
    }

    // Modal Card
    Rectangle {
        id: modalBox
        width: 440
        height: 380
        radius: FluentTheme.radiusLg
        color: FluentTheme.bgSecondary
        border.color: FluentTheme.borderHover
        border.width: 1
        anchors.centerIn: parent

        scale: root.isOpen ? 1.0 : 0.95
        Behavior on scale {
            NumberAnimation { duration: FluentTheme.animNormal; easing.type: Easing.OutBack }
        }

        MouseArea {
            anchors.fill: parent
            // Prevent clicks inside modal from closing
        }

        Column {
            anchors.fill: parent
            anchors.margins: 24
            spacing: 16

            // Header Row: Icon + Title + Close Button
            Row {
                width: parent.width
                spacing: 12

                Rectangle {
                    width: 40
                    height: 40
                    radius: 20
                    color: FluentTheme.accent
                    anchors.verticalCenter: parent.verticalCenter

                    Image {
                        source: bridge.icons.info
                        sourceSize.width: 20
                        sourceSize.height: 20
                        width: 20
                        height: 20
                        anchors.centerIn: parent
                    }
                }

                Column {
                    anchors.verticalCenter: parent.verticalCenter
                    width: parent.width - 92

                    Text {
                        text: bridge.strings.appName
                        font.family: FluentTheme.fontFamily
                        font.pixelSize: FluentTheme.fontSizeSubhead
                        font.weight: Font.DemiBold
                        color: FluentTheme.textPrimary
                        elide: Text.ElideRight
                        width: parent.width
                    }

                    Text {
                        text: "Versiyon: " + bridge.strings.version
                        font.family: FluentTheme.fontFamily
                        font.pixelSize: FluentTheme.fontSizeSmall
                        color: FluentTheme.textSecondary
                    }
                }

                // Close Button
                FluentIconButton {
                    iconSource: bridge.icons.delete
                    tooltipText: "Kapat"
                    buttonSize: 32
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked: root.isOpen = false
                }
            }

            // Divider
            Rectangle {
                width: parent.width
                height: 1
                color: FluentTheme.borderSubtle
            }

            // Content
            Column {
                width: parent.width
                spacing: 10

                Text {
                    text: "Nasıl Kullanılır?"
                    font.family: FluentTheme.fontFamily
                    font.pixelSize: FluentTheme.fontSizeBody
                    font.weight: Font.DemiBold
                    color: FluentTheme.accent
                }

                Text {
                    width: parent.width
                    wrapMode: Text.WordWrap
                    font.family: FluentTheme.fontFamily
                    font.pixelSize: FluentTheme.fontSizeSmall
                    color: FluentTheme.textPrimary
                    lineHeight: 1.4
                    text: "1. Dosya Seçimi: Resimlerinizi sol alana sürükleyip bırakın veya 'Dosya Ekle' butonunu kullanın.\n" +
                          "2. Sıralama & Yönetim: Dosyalarınızı ada veya boyuta göre sıralayabilir, çoklu seçim ile silebilirsiniz.\n" +
                          "3. İşlem Belirleme: Sağ panelden Dönüştürme, Yeniden Boyutlandırma veya Kalite Artırma seçeneğini yapılandırın.\n" +
                          "4. Başlat: 'İŞLEMİ BAŞLAT' butonuna tıklayarak işlemi tamamlayın."
                }
            }

            // Footer
            Item {
                width: parent.width
                height: 32

                Text {
                    text: bridge.strings.footerText
                    font.family: FluentTheme.fontFamily
                    font.pixelSize: FluentTheme.fontSizeSmall
                    color: FluentTheme.textSecondary
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                }

                FluentButton {
                    text: "Tamam"
                    variant: "primary"
                    implicitHeight: 32
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked: root.isOpen = false
                }
            }
        }
    }
}
