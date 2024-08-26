import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    width: 800
    height: 600
    color: "#2C2C2C" // Dark gray background

    Column{
        anchors.fill: parent
        Button {
            height: 44
            spacing: 10
            text: "Go Back"
            onClicked: {
                stackView.pop()
            }
        }
        ListView {
            id: resultsListView
            width: parent.width
            height: (parent.height - 72)
            clip: true
            model: viewHistoryScreenViewModel.results
            delegate: Item {
                width: resultsListView.width
                height: Math.max(column1.height, column2.height) + 32 // Set height to the maximum height of columns // Adjust height to fit content

                Rectangle {
                    width: parent.width
                    color: index % 2 == 0 ? "#3D3D3D" : "#4F4F4F"  // Alternating row colors
                    radius: 10
                    anchors.horizontalCenter: parent.horizontalCenter
                    border.color: index % 2 == 1 ? "#3D3D3D" : "#4F4F4F"
                    border.width: 2

                    Row {
                        spacing: 10 // Space between columns
                        anchors.fill: parent // Ensure Row fills the parent Rectangle

                        // Column 1
                        Column {
                            id: column1
                            spacing: 5
                            width: parent.width / 2 - spacing / 2 // Adjust width for each column

                            Text {
                                text: "Drill: " + model.drill_name
                                font.bold: true
                                font.pointSize: 18
                                color: "white"
                            }

                            Text {
                                text: "Start Time: " + model.start_time
                                font.pointSize: 14
                                color: "white"
                            }

                            Text {
                                text: "End Time: " + model.end_time
                                font.pointSize: 14
                                color: "white"
                            }

                            Text {
                                text: "Elapsed Time: " + model.elapsed_time + " seconds"
                                font.pointSize: 14
                                color: "white"
                            }

                            Text {
                                text: "Shots Fired: " + model.shots_fired
                                font.pointSize: 14
                                color: "white"
                            }
                        }

                        // Column 2
                        Column {
                            id: column2
                            spacing: 5
                            width: parent.width / 2 - spacing / 2 // Adjust width for each column

                            Text {
                                text: "Average Split Time: " + (model.average_split_time !== null ? model.average_split_time + " seconds" : "N/A")
                                font.pointSize: 14
                                color: "white"
                            }

                            Text {
                                text: "Fastest Split Time: " + (model.fastest_split_time !== null ? model.fastest_split_time + " seconds" : "N/A")
                                font.pointSize: 14
                                color: "white"
                            }

                            Text {
                                text: "Slowest Split Time: " + (model.slowest_split_time !== null ? model.slowest_split_time + " seconds" : "N/A")
                                font.pointSize: 14
                                color: "white"
                            }

                            Text {
                                text: "Score: " + (model.score !== null ? model.score : "N/A")
                                font.pointSize: 14
                                color: "white"
                            }

                            Text {
                                text: "Notes: " + (model.notes !== null ? model.notes : "N/A")
                                font.pointSize: 14
                                color: "white"
                                wrapMode: Text.Wrap
                            }
                        }
                    }
                }
            }

            onMovementEnded: {
                if (view.indexAt(0, height - 1) >= model.count - 1) {
                    viewHistoryScreenViewModel.loadNextPage()
                }
            }
        }
    }
}
