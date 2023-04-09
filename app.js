$(document).ready(function() {



    var basicCommands = {
        help: {
            description: 'provides a list of commands with their description to the user.',
            parameter: 'the command to get help about',
            action: '',
        },
    };

    var userCommands = {
        connect: { // the command itself
            description: 'connects the device to the nearest phone relay', // the description that appears in the help menu for this command
            parameterlist: { // the list of parameters for this command
                parameter1: {
                    description: 'the target to connect to', // description of the parameter
                    optional: false, // if the parameter has to be mandatory (default: optional)
                },
                parameter2: {
                    parameter: '-s', // if the parameter has to be a certain string
                    description: 'connect to target with the secure connection',
                },
            },
            actionlist: { // if the command should take more than one actions
                action1: {
                    text: 'connecting to #{parameter1}...', // the text it should show for this action
                    time: 3, // the time it should take to execute the next action
                },
                action2: {
                    text: 'connected to #{parameter1}',
                },
            },
        },
        disconnect: {
            description: 'disconnect from the currently connected target',
            actionList: {
                action1: {
                    text: 'disconnected',
                },
            },
        },
    };

    var commands = Object.assign(basicCommands, userCommands);




    var objectives = [];



    console.clear();

    var nickname = 'Doe';

    var keyCode = {
        enter: 13,
        arrowUp: 38,
        arrowDown: 40,
        leftArrow: 37,
        rightArrow: 39
    };

    var inputHistory = {
        backward: [],
        forward: []
    };

    var $gameContainer = $('#game');
    var $consoleInput = $('#console-input');
    var $display1 = $('#display1');
    var $consoleVisibleInput = $('#console-visible-input');
    var $startingScreen = $('#starting-screen');
    var $nicknameInput = $('#nickname');

    var $objectivesContainer = $('#objectives');

    setTimeout(function() {
        $startingScreen.addClass('showing');
    }, 1000);


});
