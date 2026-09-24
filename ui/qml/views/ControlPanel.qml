import QtQuick
import QtQuick.Controls
import ".."
import "../components"

Rectangle {
    id: root

    color: FluentTheme.bgSecondary
    border.color: FluentTheme.borderSubtle
    border.width: 1
    radius: FluentTheme.radiusLg

    Column {
        anchors.top: parent.top
        anchors.bottom: bottomSection.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 18
        anchors.bottomMargin: 14
        spacing: 16

        // Panel Title
        Text {
            text: "İşlem ve Ayarlar"
            font.family: FluentTheme.fontFamily
            font.pixelSize: FluentTheme.fontSizeTitle
            font.weight: Font.DemiBold
            color: FluentTheme.textPrimary
        }

        // Operation Segmented Tabs
        Rectangle {
            width: parent.width
            height: 40
            radius: FluentTheme.radiusMd
            color: FluentTheme.bgInput
            border.color: FluentTheme.borderSubtle
            border.width: 1

            Row {
                anchors.fill: parent
                anchors.margins: 3
                spacing: 4

                // Tab 1: Convert
                Rectangle {
                    width: (parent.width - 8) / 3
                    height: parent.height
                    radius: FluentTheme.radiusSm
                    color: bridge.currentOp === 0
                           ? FluentTheme.tabActiveBg
                           : (tab1Mouse.containsMouse ? FluentTheme.bgCardHover : "transparent")

                    border.width: bridge.currentOp === 0 ? 1 : 0
                    border.color: FluentTheme.borderHover

                    Text {
                        text: bridge.strings.tabConvert
                        anchors.centerIn: parent
                        width: parent.width - 6
                        horizontalAlignment: Text.AlignHCenter
                        elide: Text.ElideRight
                        font.family: FluentTheme.fontFamily
                        font.pixelSize: 12
                        font.weight: bridge.currentOp === 0 ? Font.DemiBold : Font.Normal
                        color: bridge.currentOp === 0 ? FluentTheme.accent : FluentTheme.textPrimary
                    }

                    MouseArea {
                        id: tab1Mouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: bridge.setCurrentOp(0)
                    }
                }

                // Tab 2: Resize
                Rectangle {
                    width: (parent.width - 8) / 3
                    height: parent.height
                    radius: FluentTheme.radiusSm
                    color: bridge.currentOp === 1
                           ? FluentTheme.tabActiveBg
                           : (tab2Mouse.containsMouse ? FluentTheme.bgCardHover : "transparent")

                    border.width: bridge.currentOp === 1 ? 1 : 0
                    border.color: FluentTheme.borderHover

                    Text {
                        text: bridge.strings.tabResize
                        anchors.centerIn: parent
                        width: parent.width - 6
                        horizontalAlignment: Text.AlignHCenter
                        elide: Text.ElideRight
                        font.family: FluentTheme.fontFamily
                        font.pixelSize: 12
                        font.weight: bridge.currentOp === 1 ? Font.DemiBold : Font.Normal
                        color: bridge.currentOp === 1 ? FluentTheme.accent : FluentTheme.textPrimary
                    }

                    MouseArea {
                        id: tab2Mouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: bridge.setCurrentOp(1)
                    }
                }

                // Tab 3: Enhance
                Rectangle {
                    width: (parent.width - 8) / 3
                    height: parent.height
                    radius: FluentTheme.radiusSm
                    color: bridge.currentOp === 2
                           ? FluentTheme.tabActiveBg
                           : (tab3Mouse.containsMouse ? FluentTheme.bgCardHover : "transparent")

                    border.width: bridge.currentOp === 2 ? 1 : 0
                    border.color: FluentTheme.borderHover

                    Text {
                        text: bridge.strings.tabEnhance
                        anchors.centerIn: parent
                        width: parent.width - 6
                        horizontalAlignment: Text.AlignHCenter
                        elide: Text.ElideRight
                        font.family: FluentTheme.fontFamily
                        font.pixelSize: 12
                        font.weight: bridge.currentOp === 2 ? Font.DemiBold : Font.Normal
                        color: bridge.currentOp === 2 ? FluentTheme.accent : FluentTheme.textPrimary
                    }

                    MouseArea {
                        id: tab3Mouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: bridge.setCurrentOp(2)
                    }
                }
            }
        }

        // Dynamic Options Card
        FluentCard {
            width: parent.width
            implicitHeight: dynamicContent.implicitHeight + 28

            Column {
                id: dynamicContent
                anchors.fill: parent
                anchors.margins: 14
                spacing: 12

                // --- Op 0: Convert Options ---
                Column {
                    visible: bridge.currentOp === 0
                    width: parent.width
                    spacing: 8

                    Text {
                        text: bridge.strings.targetFormat
                        font.family: FluentTheme.fontFamily
                        font.pixelSize: FluentTheme.fontSizeBody
                        font.weight: Font.DemiBold
                        color: FluentTheme.textPrimary
                    }

                    FluentComboBox {
                        width: parent.width
                        model: bridge.supportedFormats
                        currentIndex: bridge.supportedFormats.indexOf(bridge.targetFormat) >= 0 ? bridge.supportedFormats.indexOf(bridge.targetFormat) : 1
                        onActivated: (index) => {
                            bridge.setTargetFormat(bridge.supportedFormats[index]);
                        }
                    }
                }

                // --- Op 1: Resize Options ---
                Column {
                    visible: bridge.currentOp === 1
                    width: parent.width
                    spacing: 10

                    Column {
                        width: parent.width
                        spacing: 6

                        Text {
                            text: bridge.strings.resizeMethod
                            font.family: FluentTheme.fontFamily
                            font.pixelSize: FluentTheme.fontSizeBody
                            font.weight: Font.DemiBold
                            color: FluentTheme.textPrimary
                        }

                        // Full width segmented method switcher
                        Rectangle {
                            width: parent.width
                            height: 36
                            radius: FluentTheme.radiusSm
                            color: FluentTheme.bgInput
                            border.color: FluentTheme.borderSubtle
                            border.width: 1

                            Row {
                                anchors.fill: parent
                                anchors.margins: 2
                                spacing: 2

                                Rectangle {
                                    width: (parent.width - 2) / 2
                                    height: parent.height
                                    radius: FluentTheme.radiusSm
                                    color: bridge.resizeType === 0 ? (FluentTheme.isDark ? "#4E2C39" : "#FFFFFF") : "transparent"
                                    border.width: bridge.resizeType === 0 ? 1 : 0
                                    border.color: FluentTheme.borderHover

                                    Text {
                                        text: bridge.strings.methodDimensions
                                        anchors.centerIn: parent
                                        font.family: FluentTheme.fontFamily
                                        font.pixelSize: FluentTheme.fontSizeSmall
                                        font.weight: bridge.resizeType === 0 ? Font.DemiBold : Font.Normal
                                        color: bridge.resizeType === 0 ? FluentTheme.accent : FluentTheme.textPrimary
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: bridge.setResizeType(0)
                                    }
                                }

                                Rectangle {
                                    width: (parent.width - 2) / 2
                                    height: parent.height
                                    radius: FluentTheme.radiusSm
                                    color: bridge.resizeType === 1 ? (FluentTheme.isDark ? "#4E2C39" : "#FFFFFF") : "transparent"
                                    border.width: bridge.resizeType === 1 ? 1 : 0
                                    border.color: FluentTheme.borderHover

                                    Text {
                                        text: bridge.strings.methodPercent
                                        anchors.centerIn: parent
                                        font.family: FluentTheme.fontFamily
                                        font.pixelSize: FluentTheme.fontSizeSmall
                                        font.weight: bridge.resizeType === 1 ? Font.DemiBold : Font.Normal
                                        color: bridge.resizeType === 1 ? FluentTheme.accent : FluentTheme.textPrimary
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: bridge.setResizeType(1)
                                    }
                                }
                            }
                        }
                    }

                    // Dimensions input
                    Row {
                        visible: bridge.resizeType === 0
                        width: parent.width
                        spacing: 10

                        Column {
                            width: (parent.width - 10) / 2
                            spacing: 4
                            Text {
                                text: bridge.strings.width
                                font.family: FluentTheme.fontFamily
                                font.pixelSize: FluentTheme.fontSizeSmall
                                color: FluentTheme.textSecondary
                            }
                            FluentSpinBox {
                                width: parent.width
                                from: 1
                                to: 10000
                                stepSize: 10
                                suffix: " px"
                                value: bridge.resizeWidth
                                onValueModified: (v) => bridge.setResizeWidth(v)
                            }
                        }

                        Column {
                            width: (parent.width - 10) / 2
                            spacing: 4
                            Text {
                                text: bridge.strings.height
                                font.family: FluentTheme.fontFamily
                                font.pixelSize: FluentTheme.fontSizeSmall
                                color: FluentTheme.textSecondary
                            }
                            FluentSpinBox {
                                width: parent.width
                                from: 1
                                to: 10000
                                stepSize: 10
                                suffix: " px"
                                value: bridge.resizeHeight
                                onValueModified: (v) => bridge.setResizeHeight(v)
                            }
                        }
                    }

                    // Percentage input
                    Column {
                        visible: bridge.resizeType === 1
                        width: parent.width
                        spacing: 4

                        Text {
                            text: bridge.strings.percent
                            font.family: FluentTheme.fontFamily
                            font.pixelSize: FluentTheme.fontSizeSmall
                            color: FluentTheme.textSecondary
                        }

                        FluentSpinBox {
                            width: parent.width
                            from: 1
                            to: 500
                            stepSize: 5
                            suffix: " %"
                            value: bridge.resizePercent
                            onValueModified: (v) => bridge.setResizePercent(v)
                        }
                    }
                }

                // --- Op 2: Enhance Options ---
                Column {
                    visible: bridge.currentOp === 2
                    width: parent.width
                    spacing: 8

                    Text {
                        text: bridge.strings.enhanceFactor
                        font.family: FluentTheme.fontFamily
                        font.pixelSize: FluentTheme.fontSizeBody
                        font.weight: Font.DemiBold
                        color: FluentTheme.textPrimary
                    }

                    FluentSpinBox {
                        width: parent.width
                        from: 1.1
                        to: 4.0
                        stepSize: 0.5
                        decimals: 1
                        suffix: " x"
                        value: bridge.enhanceFactor
                        onValueModified: (v) => bridge.setEnhanceFactor(v)
                    }
                }
            }
        }

        // Target Folder Card
        FluentCard {
            width: parent.width
            implicitHeight: folderCol.implicitHeight + 24

            Column {
                id: folderCol
                anchors.fill: parent
                anchors.margins: 12
                spacing: 8

                Text {
                    text: bridge.strings.targetFolder
                    font.family: FluentTheme.fontFamily
                    font.pixelSize: FluentTheme.fontSizeBody
                    font.weight: Font.DemiBold
                    color: FluentTheme.textPrimary
                }

                // Path display & Action buttons
                Row {
                    width: parent.width
                    spacing: 6

                    Rectangle {
                        width: parent.width - 76
                        height: 34
                        radius: FluentTheme.radiusSm
                        color: FluentTheme.bgInput
                        border.color: FluentTheme.borderSubtle
                        border.width: 1

                        Text {
                            anchors.fill: parent
                            anchors.leftMargin: 8
                            anchors.rightMargin: 8
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideMiddle
                            text: bridge.outputDir || bridge.strings.outputPlaceholder
                            font.family: FluentTheme.fontFamily
                            font.pixelSize: FluentTheme.fontSizeSmall
                            color: FluentTheme.textSecondary
                        }
                    }

                    // Browse folder button
                    FluentIconButton {
                        iconSource: bridge.icons.folder
                        tooltipText: bridge.strings.tooltipOpenFolder
                        buttonSize: 34
                        onClicked: bridge.browseOutputDir()
                    }

                    // Open output folder directly in Windows Explorer (Requirement 4)
                    FluentIconButton {
                        iconSource: bridge.icons.openFolder
                        tooltipText: bridge.strings.tooltipOpenFolder
                        buttonSize: 34
                        onClicked: bridge.openOutputFolder()
                    }
                }
            }
        }
    }

    // Pinned Bottom Section: Progress and Action Button
    Column {
        id: bottomSection
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 18
        spacing: 12

        // Progress & Status Section
        Column {
            width: parent.width
            spacing: 8

            Item {
                width: parent.width
                height: 18

                Text {
                    text: bridge.progressMessage
                    font.family: FluentTheme.fontFamily
                    font.pixelSize: FluentTheme.fontSizeSmall
                    color: FluentTheme.textSecondary
                    elide: Text.ElideRight
                    anchors.left: parent.left
                    anchors.right: pctText.left
                    anchors.rightMargin: 8
                    anchors.verticalCenter: parent.verticalCenter
                }

                Text {
                    id: pctText
                    visible: bridge.isProcessing
                    text: bridge.progressValue + "%"
                    font.family: FluentTheme.fontFamily
                    font.pixelSize: FluentTheme.fontSizeSmall
                    font.weight: Font.DemiBold
                    color: FluentTheme.accent
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            FluentProgressBar {
                width: parent.width
                value: bridge.progressValue
                indeterminate: bridge.isProcessing && bridge.progressValue === 0
            }
        }

        // Primary Action Button (Start / Process)
        FluentButton {
            width: parent.width
            implicitHeight: 44
            variant: "primary"
            text: bridge.isProcessing ? "İptal Et" : bridge.strings.btnProcess
            enabled: bridge.totalCount > 0 || bridge.isProcessing
            onClicked: {
                if (bridge.isProcessing) {
                    bridge.cancelProcessing();
                } else {
                    bridge.startProcessing();
                }
            }
        }
    }
}
