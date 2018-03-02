<?php
//变量array
$method = $argv[1];
$value = array("aaa"=>1,"bbb"=>2,"ccc"=>array(1,2));

function array_json()
{
    $aa =array("aaa"=>1,"bbb"=>2,"ccc"=>array(1,2));
    echo json_encode($aa);
    echo "好的";
}


