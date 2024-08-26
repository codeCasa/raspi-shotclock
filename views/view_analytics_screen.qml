import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    width: 800
    height: 600
    color: "#2C2C2C" // Dark gray background

    Column {
        anchors.fill: parent
        spacing: 20

        Row{
            
            Button {
                text: "Go Back"
                spacing: 10
                onClicked: {
                    stackView.pop()
                }
            }

            Row {
                spacing: 10

                Button {
                    text: "Prev Week"
                    onClicked: viewAnalyticsScreenViewModel.previousWeek()
                }

                Text {
                    id: timeSpanText
                    text: viewAnalyticsScreenViewModel.timeSpan
                    color: "white"
                    font.pointSize: 16
                    font.bold: true
                }

                Button {
                    text: "Next Week"
                    onClicked: viewAnalyticsScreenViewModel.nextWeek()
                    enabled: viewAnalyticsScreenViewModel.nextButtonEnabled
                }
            }
        }

        Text {
            text: "Analysis for " + viewAnalyticsScreenViewModel.drillName
            font.pointSize: 20
            color: "white"
            font.bold: true
        }

        Image {
            source: viewAnalyticsScreenViewModel.plotUrl
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width - 40
            height: parent.height - 100
            fillMode: Image.PreserveAspectFit
            visible: viewAnalyticsScreenViewModel.hasDrills
        }

        Text {
            text: "No drills found for this week"
            font.pointSize: 20
            color: "white"
            font.bold: true
            visible: !viewAnalyticsScreenViewModel.hasDrills
        }
    }
}
