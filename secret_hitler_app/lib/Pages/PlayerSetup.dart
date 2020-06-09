class Page_PlayerSetup extends StatefulWidget {
  /*  Player Setup
        Generates a form to gather the number of players and player names
   */

  @override
  _Page_PlayerSetupState createState() => _Page_PlayerSetupState();
}

class _Page_PlayerSetupState extends State<Page_PlayerSetup> {
  var minPlayers = 5;
  var maxPlayers = 10;
  var numPlayers = 5;

  final _formKey = GlobalKey<FormState>();

  List<String> names = [];

  @override
  Widget build(BuildContext context) {
    names = []; // Resets the name list each time
    return Scaffold(
      backgroundColor: Colors.blueGrey[800],
      appBar: AppBar(
        title: Text("Player Setup", style: TextStyle(fontSize: 24)),
      ),
      body: Center(
        child: Padding(
          padding: EdgeInsets.all(15.0),
          child: Column(
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(
                  "Player Names",
                  style: TextStyle(
                    fontSize: 20,
                    color: Colors.white,
                  ),
                ),
              ),
              Expanded(
                flex: 4,
                child: ListView(
                  children: [
                    Form(
                      key: _formKey, // Used for the validation step
                      child:
                          GetForm_playerNames(), // Returns a TextFormField with the appropriate number of name fields
                    ),
                  ],
                ),
              ),
              Expanded(
                flex: 2,
                child: GetAddRemoveButtons(),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget GetForm_playerNames() {
    var playerForm = List<Widget>();
    for (var player = 0; player < numPlayers; player++) {
      playerForm.add(TextFormField(
        decoration: const InputDecoration(
          hintText: 'Enter player name',
          enabledBorder: UnderlineInputBorder(
            borderSide: BorderSide(color: Colors.white),
          ),
          hintStyle: TextStyle(
            color: Colors.white,
          ),
        ),
        style: TextStyle(
          color: Colors.white,
        ),
        validator: (String value) {
          if (value.isEmpty) {
            return 'Please input a name';
          }
          names.add(value);
          return null;
        },
      ));
    }
    return Column(children: playerForm);
  }

  Widget GetAddRemoveButtons() {
    var buttonList = List<Widget>();

    if (numPlayers < maxPlayers) {
      buttonList.add(Expanded(
        child: BuildButton(context, "Add", () {
          numPlayers++;
          setState(() {});
        }),
      ));
    }
    if (numPlayers > minPlayers) {
      buttonList.add(Expanded(
          child: BuildButton(context, "Remove", () {
        numPlayers--;
        setState(() {});
      })));
    }
    buttonList.add(Expanded(
      child: BuildButton(context, "Begin", () {
        if (_formKey.currentState.validate()) {
          Navigator.push(context,
              MaterialPageRoute(builder: (context) => new Board(names: names)));
          setState(() {});
        }
      }),
    ));
    return Center(
      child: Row(
        children: buttonList,
        mainAxisAlignment: MainAxisAlignment.center,
      ),
    );
  }

  Widget BuildButton(BuildContext context, String text, VoidCallback callback) {
    return Padding(
      padding: EdgeInsets.all(8.0),
      child: ButtonTheme(
        minWidth: 10,
        height: 50,
        child: RaisedButton(
          textColor: Colors.yellow[300],
          color: Colors.deepOrange[800],
          child: Text(text, style: TextStyle(fontSize: 18)),
          shape: RoundedRectangleBorder(
            side: BorderSide(
              color: Colors.yellow[300],
              width: 1,
            ),
            borderRadius: BorderRadius.all(Radius.circular(30)),
          ),
          onPressed: callback,
        ),
      ),
    );
  }
}
