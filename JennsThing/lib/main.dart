import 'package:flutter/material.dart';
import 'Patient.dart';
import "Parameters.dart";

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  /* Main body of website*/
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final _formKey = GlobalKey<FormState>();
  static var _patient = Patient();
  var displayFlag = false;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // Title, Theme, Home:
      theme: ThemeData(
        primaryColor: Colors.blueGrey[400],
      ),
      home: Scaffold(
        appBar: AppBar(
          title: Text("Jenn's Thing"),
          centerTitle: true,
        ),
        backgroundColor: Colors.white,
        body: Column(
          children: getBody(),
        ),
      ),
    );
  }

  Widget getWeight() {
    Widget playerForm = TextFormField(
      decoration: const InputDecoration(
        hintText: 'Enter patient weight',
        enabledBorder: UnderlineInputBorder(
          borderSide: BorderSide(color: Colors.blueAccent),
        ),
        hintStyle: TextStyle(
          color: Colors.black,
        ),
      ),
      style: TextStyle(
        color: Colors.black,
      ),
      validator: (String value) {
        if (value.isEmpty) {
          return 'Please input a name';
        }
        _patient.setPatientWeight(value);
        _patient.doItAll();
        return null;
      },
    );
    return Container(
      child: playerForm,
    );
  }

  Widget answerCard(var title, var text) {
    return Card(
      color: Colors.grey[200],
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            ListTile(
              title: Text(title,
                  style: TextStyle(
                    fontSize: 24,
                  )),
              subtitle: Text(text),
            ),
          ],
        ),
      ),
    );
  }

  Widget startButton() {
    return ButtonTheme(
      minWidth: 150,
      height: 50,
      child: RaisedButton(
        textColor: Colors.grey[300],
        color: Colors.blueAccent,
        child: Text(
          "Start",
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        shape: RoundedRectangleBorder(
          side: BorderSide(
            color: Colors.blue[800],
            width: 1,
          ),
          borderRadius: BorderRadius.all(Radius.circular(30)),
        ),
        onPressed: () {
          setState(() {
            displayFlag = true;
            _formKey.currentState.validate();
          });
        },
      ),
    );
  }

  List<Widget> getBody() {
    List<Widget> body = [];
    // Patient Weight Input Field
    body.add(
      Padding(
        padding: const EdgeInsets.fromLTRB(150.0, 0.0, 150.0, 0.0),
        child: Form(
          key: _formKey, // Used for the validation step
          child:
              getWeight(), // Returns a TextFormField with the appropriate number of name fields
        ),
      ),
    );
    // Start button
    body.add(
      Padding(
        padding: const EdgeInsets.all(8.0),
        child: startButton(),
      ),
    );

    // After the patient weight has been added, display the results
    if (displayFlag) {
      // Display input weight
      body.add(
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Text("Patient Weight: ${_patient.patientWeight}"),
        ),
      );
      // Section 1 Tile
      body.add(
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: answerCard("Section 1: ",
              "\tCalories: ${_patient.caloricNeeds_min} - ${_patient.caloricNeeds_max} kcal/day\n\tProtein: ${_patient.proteinNeeds_min} - ${_patient.proteinNeeds_max} g/day\n\tAdjusted Calories: ${_patient.scaledCaloricNeeds_min} - ${_patient.scaledCaloricNeeds_max} kcal/day"),
        ),
      );
      // Section 2 Tile
      body.add(
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: answerCard("Section 2: ",
              "\tCalorie Average: ${_patient.averageCaloricNeeds} kcal/day\n\tProtein Average: ${_patient.averageProteinRounded} (${_patient.averageProteinNeeds}) g/day"),
        ),
      );
      // Section 3 Tile
      body.add(
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Card(
            color: Colors.grey[200],
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  ListTile(
                    title: Text("Section 3",
                        style: TextStyle(
                          fontSize: 24,
                        )),
                  ),
                  Padding(
                    padding: const EdgeInsets.fromLTRB(32.0, 0.0, 0.0, 0.0),
                    child: Table(////////////// Make a for loop here?
                        children: [
                      TableRow(children: [
                        Text(
                          "AA Concentration (%)",
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          "Solution Volume (ml)",
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          "Rounded Rate (ml/hour)",
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          "Updated Volume (l/day)??",
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          "Updated Calories (kcal/day)",
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          "Updated Protein (g/day)",
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ]),
                      TableRow(children: [
                        Text("${aminoAcidConcentrations[0]}"),
                        Text(
                            "${_patient.aminoAcidSolution[0].toStringAsFixed(1)}"),
                        Text("${_patient.hourlyRate[0].toStringAsFixed(1)}"),
                        Text("${_patient.updatedVolume[0].toStringAsFixed(1)}"),
                        Text(
                            "${_patient.updatedCalories[0].toStringAsFixed(1)}"),
                        Text(
                            "${_patient.updatedProtein[0].toStringAsFixed(1)}"),
                      ]),
                      TableRow(children: [
                        Text("${aminoAcidConcentrations[1]}"),
                        Text(
                            "${_patient.aminoAcidSolution[1].toStringAsFixed(1)}"),
                        Text("${_patient.hourlyRate[1].toStringAsFixed(1)}"),
                        Text("${_patient.updatedVolume[1].toStringAsFixed(1)}"),
                        Text(
                            "${_patient.updatedCalories[1].toStringAsFixed(1)}"),
                        Text(
                            "${_patient.updatedProtein[1].toStringAsFixed(1)}"),
                      ]),
                      TableRow(children: [
                        Text("${aminoAcidConcentrations[2]}"),
                        Text(
                            "${_patient.aminoAcidSolution[2].toStringAsFixed(1)}"),
                        Text("${_patient.hourlyRate[2].toStringAsFixed(1)}"),
                        Text("${_patient.updatedVolume[2].toStringAsFixed(1)}"),
                        Text(
                            "${_patient.updatedCalories[2].toStringAsFixed(1)}"),
                        Text(
                            "${_patient.updatedProtein[2].toStringAsFixed(1)}"),
                      ]),
                    ]),
                  )
                ],
              ),
            ),
          ),
        ),
      );

      body.add(getTableTile(0));
    }
    return body;
  }

  Widget getTableTile(int index) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Card(
        color: Colors.grey[200],
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
//          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              title: Text(
                  "AA Concentration: ${_patient.aminoAcidSolution[index].toStringAsFixed(1)}",
                  style: TextStyle(
                    // TODO: Make uniform via function
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  )),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(32.0, 0.0, 0.0, 0.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                      "Solution Volume (ml): \t\t${_patient.aminoAcidSolution[index].toStringAsFixed(1)}"),
                  Text(
                      "Rounded Rate (ml/hour): \t  ${_patient.hourlyRate[index].toStringAsFixed(1)}"),
                  Text(
                      "Updated Volume (/day?): \t${_patient.updatedVolume[index].toStringAsFixed(1)}"),
                  Text(
                      "Updated Calories (kcal/day): \t${_patient.updatedCalories[index].toStringAsFixed(1)}"),
                  Text(
                      "Updated Protein (g/day): \t${_patient.updatedProtein[index].toStringAsFixed(1)}"),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
