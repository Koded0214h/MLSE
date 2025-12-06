// Here is the hierarchy, followed by a code example that includes all the major 
// task types: Synchronous Code, process.nextTick(), Promises (Micro-tasks), 
// and Timers (setTimeout/setImmediate - Macro-tasks).

// 1. Synchronous code: console.log(), simple functions, loops -- highest
// 2. `process.nextTick()`: process.nextTick(() => {...})
// 3. Other micro-task: Promise.resolve().then(...)
// 4. Macro-task: setTimeout(0), I/O Callbacks, setImmediate() -- lowest


// ---------------------------------
// Full Priority Code Demo
// ---------------------------------

console.log("1. SYNC START (Executes Immediately)");

// 3. --- PROMISE (Lower Micro-task Priority) ---
Promise.resolve().then(() => {
    console.log("3. PROMISE (Micro-task, after nextTick)");
});

// 2. --- NEXT TICK (Highest Micro-task Priority) ---
process.nextTick(() => {
    console.log("2. NEXT TICK (Highest Micro-task)");
});

// 4. --- SET TIMEOUT (Lowest Priority Macro-task) ---
setTimeout(() => {
    console.log("4. SET TIMEOUT (Macro-task, runs last)");
}, 0);

console.log("5. SYNC END (Executes Immediately)");