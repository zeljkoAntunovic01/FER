var express = require('express');
var router = express.Router();
var db = require("../db/index");
var { body, validationResult } = require('express-validator');

router.get('/:id([0-9])', async function(req, res) {

    let id = parseInt(req.params.id);

    var item = (await db.query("SELECT * FROM inventory WHERE id = $1", [id])).rows[0];

    if (!item){
        res.status(404).send("Item does not exist.");
    }else {
        var category = (await db.query("SELECT * FROM categories WHERE id = $1", [item.categoryid])).rows[0];

        res.render('item', {
            title: item.name,
            linkActive: 'order',
            item,
            category,
            index: id
        });
    }

})

module.exports = router