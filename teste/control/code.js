
////////////////////////////////////////////
// Initialize the custom control
WebCC.start(
  // callback function; occurs when the connection is done or failed. 
  // "result" is a boolean defining if the connection was successfull or not.
  function (result) {
    if (result) {
      console.log('connected successfully');
      // Set current values
      // Subscribe for value changes
      WebCC.onPropertyChanged.subscribe(setProperty);
    }
    else {
      console.log('connection failed');
    }
  },
  // contract (see also manifest.json)
  {
    // Methods
    methods: {
    },
    // Events
    events: ['ZoneChanged'],
    // Properties
    properties: {
      GaugeValue: 20,
      GaugeBackColor: 4294967295,
      Alignment:
      {
        Vertical: 'Center'
      },
      LineThickness: 20,
      FontSize: 16,
      MinValue: 0,
      MaxValue: 50,
      DivisionCount: 5,
      Zones: [
        { Min: 0, Max: 30, StrokeColor: 4281381677 },
        { Min: 30, Max: 40, StrokeColor: 4294958336 },
        { Min: 40, Max: 50, StrokeColor: 4293934654 }
      ]
    }
  },
  // placeholder to include additional Unified dependencies (not used in this example)
  [],
  // connection timeout
  10000
);