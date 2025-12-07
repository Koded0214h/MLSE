// For TypeScript

const enum LoggingLevel {
    DEBUG = 0,
    INFO = 1,
    ERROR = 2
}

// compiled javasript (equivalent)
// const enum is completely removed/inlined;
// console.log(0);
// comsole.log(1);

console.log(LoggingLevel.DEBUG);
console.log(LoggingLevel.INFO);