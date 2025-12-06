console.log("1. Program Start: Synchronous code begins.");

// --- I/O-Bound Task (Delegated to Web/Node API) ---
setTimeout(() => {
    // This is the callback function. It goes to the Callback Queue.
    console.log("4. I/O Task Complete: This message was delayed but NOT blocking the main thread.");
}, 0); // Request to run this callback after 0ms (as soon as possible)

// --- CPU-Bound Task (Blocks the Single Thread) ---
const startTime = Date.now();
while(Date.now() - startTime < 3000) {
    // This loop simulates a heavy calculation that takes 3 seconds -- 3000ms.
    // The single thread is STUCK here, regardless of the 'setTimeout(..., 0)' above.
}

console.log("3. CPU Task Complete: This synchronous task blocked the thread for 3 seconds.");

console.log("2. Program End: Synchronous code finishes.");

console.log("=============================================");
console.log("=============================================");

// Macro VS Micro Tasks

console.log("1. Program Start (Synchronous)");

// --- A. Macro-task (Timer Queue) ---
setTimeout(() => {
    console.log("3. Macro-task: setTimeout(0) runs last.");
}, 0);

// --- B. Micro-task (Promise Queue) ---
Promise.resolve()
    .then(() => {
        console.log("2. Micro-task: Promise runs immediately after sync code.");
    });

console.log("4. Program End (Synchronous)");

console.log("=============================================");
console.log("=============================================");

