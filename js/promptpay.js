/**
 * BioRevive Lab - PromptPay QR Code Generator (Standalone)
 * Based on EMVCo Standard
 */
function generatePromptPayPayload(id, amount) {
    const target = id.replace(/[^0-9]/g, '');
    let targetType = target.length >= 13 ? '03' : '01'; // 03 for ID, 01 for Mobile
    
    // Formatting for 10-digit mobile
    let formattedTarget = target;
    if (targetType === '01') {
        formattedTarget = "0066" + target.substring(1);
        formattedTarget = formattedTarget.padStart(13, '0');
    }

    let payload = [
        f("00", "01"), // Payload Format Indicator
        f("01", "11"), // Point of Initiation Method (11 = Static, 12 = Dynamic)
        f("29", [
            f("00", "A000000677010111"), // AID
            f(targetType, formattedTarget)
        ].join('')),
        f("53", "764"), // Currency (764 = THB)
        f("54", amount.toFixed(2)), // Transaction Amount
        f("58", "TH") // Country Code
    ].join('');

    // CRC16
    payload += "6304";
    payload += crc16(payload).toString(16).toUpperCase().padStart(4, '0');
    
    return payload;
}

function f(id, val) {
    return id + val.length.toString().padStart(2, '0') + val;
}

function crc16(data) {
    let crc = 0xFFFF;
    for (let i = 0; i < data.length; i++) {
        let x = ((crc >> 8) ^ data.charCodeAt(i)) & 0xFF;
        x ^= x >> 4;
        crc = ((crc << 8) ^ (x << 12) ^ (x << 5) ^ x) & 0xFFFF;
    }
    return crc;
}
