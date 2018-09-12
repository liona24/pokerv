export function createRoom(socket, roomName, size, stackSize, bigBlind, smallBlind) {

    console.log(`createRoom( ${socket}, ${roomName}, ${size}, ${stackSize}, ${bigBlind}, ${smallBlind} )`);

    return new Promise((resolve) =>
        socket.emit('create', {
            room: roomName,
            size: size,
            bigblind: bigBlind,
            smallblind: smallBlind,
            stacksize: stackSize
        }, resolve)
    );
}

export function joinRoom(socket, roomName, userName, playerType) {

    console.log(`joinRoom( ${socket}, ${roomName}, ${userName}, ${playerType} )`);

    return new Promise((resolve) =>
        socket.emit('join', {
            room: roomName,
            user: userName,
            player_type: playerType
        }, resolve)
    );
}

export function move(socket, roomName, playerName, betsize) {

    console.log(`move( ${socket}, ${roomName}, ${playerName}, ${betsize})`);

    return new Promise((resolve) =>
        socket.emit('finished move', {
            name: playerName,
            room: roomName,
            betsize: betsize
        }, resolve)
    );
}