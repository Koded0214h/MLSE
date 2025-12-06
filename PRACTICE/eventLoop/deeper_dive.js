//  1. Outside an I/O Cycle (Main Module Execution)

// setTimeout & setImmediate
setTimeout(() => {
    console.log("Timeout");
}, 0)

setImmediate(() => {
    console.log("Immediate");
})

// Output could be: 'Timeout', 'Immediate'
// OR: 'Immediate', 'Timeout'

// 2. Inside an I/O Cycle (Deterministic Behavior)

// The I/O operation finishes, and its callback executes in the Poll phase.
// The callback finishes, and the Event Loop proceeds to the Check phase.
// setImmediate() callbacks (placed in the Check phase) are executed.
// The loop moves to the next cycle and enters the Timers phase.
// setTimeout(0) callbacks (placed in the Timers phase) are executed.

const fs = require('fs');
fs.readFile('../resources/file.txt', () => { // We are now in the I/O Poll Phase
    setTimeout(() => {
        console.log('Timeout (Second)');
    }, 0);

    setImmediate(() => {
        console.log('Immediate (First)');
    })
})

// Output will ALWAYS be: 'Immediate (First)', 'Timeout (Second)'