var express = require('express');
var router = express.Router();
var db = require("../db/index");

router.get('/', async function(req, res, next) {

    var categories = (await db.query('SELECT * FROM categories ORDER BY id asc')).rows;
    var inventory = (await db.query('SELECT * FROM inventory ORDER BY id asc')).rows;

    categories.forEach(function (category){
        category.inv = []
        inventory.forEach(function (item){
            if (item.categoryid == category.id){
                category.inv.push(item);
            }
        });
    });
   

    res.render('order', {
        title: 'Order',
        linkActive: 'order',
        categories: categories,
    });
});

module.exports = router