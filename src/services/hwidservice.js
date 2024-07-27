const hwidKeys = {};

exports.checkHWID = (req, res) => {
    const hwid = req.query.hwid;
    if (hwidKeys[hwid]) {
        res.json({ status: 'success', hasKey: true, key: hwidKeys[hwid] });
    } else {
        res.json({ status: 'success', hasKey: false });
    }
};

exports.setKey = (hwid, key) => {
    hwidKeys[hwid] = key;
};
