import QtQuick

pragma Singleton

QtObject {
    id: theme

    // Set by Main.qml according to bridge.currentTheme
    property bool isDark: true

    // Typography
    readonly property string fontFamily: "Segoe UI Variable Display, Segoe UI, sans-serif"
    readonly property int fontSizeSmall: 11
    readonly property int fontSizeBody: 13
    readonly property int fontSizeSubhead: 14
    readonly property int fontSizeTitle: 18
    readonly property int fontSizeHeader: 22

    // Radiuses
    readonly property real radiusSm: 4
    readonly property real radiusMd: 8
    readonly property real radiusLg: 12
    readonly property real radiusXl: 16

    // Animation Durations
    readonly property int animFast: 150
    readonly property int animNormal: 250

    // Dynamic Colors based on isDark
    readonly property color bgApp: isDark ? "#202020" : "#F3F3F3"
    readonly property color bgSecondary: isDark ? "#272727" : "#FFFFFF"
    readonly property color bgCard: isDark ? "#2C2C2C" : "#FFFFFF"
    readonly property color bgCardHover: isDark ? "#333333" : "#F8F8F8"
    readonly property color bgCardActive: isDark ? "#262626" : "#F0F0F0"
    readonly property color bgInput: isDark ? "#1F1F1F" : "#FFFFFF"
    
    readonly property color borderSubtle: isDark ? "#383838" : "#E2E2E2"
    readonly property color borderCard: isDark ? "#3A3A3A" : "#E5E5E5"
    readonly property color borderHover: isDark ? "#4F4F4F" : "#CCCCCC"
    
    readonly property color textPrimary: isDark ? "#FFFFFF" : "#1A1A1A"
    readonly property color textSecondary: isDark ? "#A0A0A0" : "#606060"
    readonly property color textMuted: isDark ? "#707070" : "#8A8A8A"
    
    readonly property color accent: isDark ? "#4CC2FF" : "#0067C0"
    readonly property color accentHover: isDark ? "#58C8FF" : "#1878D0"
    readonly property color accentActive: isDark ? "#38B4F5" : "#005BA6"
    readonly property color accentText: "#FFFFFF"
    readonly property color tabActiveBg: isDark ? "#1E3A4E" : "#CFEAF9"
    
    readonly property color danger: isDark ? "#FF5555" : "#C42B1C"
    readonly property color dangerHover: isDark ? "#FF6E6E" : "#D1382A"
    readonly property color dangerBg: isDark ? "#381E20" : "#FDE7E9"
    
    readonly property color success: isDark ? "#6CCB5F" : "#0F7B0F"
    readonly property color successBg: isDark ? "#1C3320" : "#DFF6DD"
    
    readonly property color warning: isDark ? "#FCE100" : "#9D5D00"
    readonly property color warningBg: isDark ? "#3B331A" : "#FFF4CE"
}
