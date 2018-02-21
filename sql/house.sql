# create database house;

drop table `community`;
CREATE TABLE `community` (
`id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`name` varchar(30) NOT NULL DEFAULT '' COMMENT '小区名称',
`link_community_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '链家小区id',
`image` varchar(500) NOT NULL DEFAULT '' COMMENT '小区缩略图',
`url` varchar(500) NOT NULL DEFAULT '' COMMENT '小区url',
`district` varchar(10) NOT NULL DEFAULT '' COMMENT '所在区域',
`address` varchar(20) NOT NULL DEFAULT '' COMMENT '所在小区域',
`building_type` varchar(50) NOT NULL DEFAULT '' COMMENT '建筑类型',
`year` int(11) NOT NULL DEFAULT 0 COMMENT '建筑年份',
`subway_tag` varchar(50) NOT NULL DEFAULT '' COMMENT '地铁标签',
`price` int(11) NOT NULL DEFAULT 0 COMMENT '小区单价',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='小区表';




drop table `community_price`;
CREATE TABLE `community_history_price` (
`id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`link_community_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '链家小区id',
`month` int(11) NOT NULL DEFAULT 0 COMMENT '月份',
`price` int(11) NOT NULL DEFAULT 0 COMMENT '小区单价',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='小区历史价格表';



drop table `community_sale`;
CREATE TABLE `community_sale` (
`id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`link_community_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '链家小区id',
`month_deal` int(11) NOT NULL DEFAULT 0 COMMENT '30天成交数',
`on_sale` int(11) NOT NULL DEFAULT 0 COMMENT '在售二手房数',
`lease` int(11) NOT NULL DEFAULT 0 COMMENT '正在出租数',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='小区销售数据表';







drop table `house_source`;
CREATE TABLE `house_source` (
`id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`link_house_source_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '房源id',
`url` varchar(500) NOT NULL DEFAULT '' COMMENT '房源url',
`title_discribe` varchar(500) NOT NULL DEFAULT '' COMMENT '房源描述',
`community_name` varchar(30) NOT NULL DEFAULT '' COMMENT '小区名称',
`link_community_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '链家小区id',
`home_plan_structure` varchar(20) NOT NULL DEFAULT '' COMMENT '户型结构',
`building_size` double NOT NULL DEFAULT 0 COMMENT '平米数',
`orientation` varchar(20) NOT NULL DEFAULT '' COMMENT '朝向',
`decorate_situation` varchar(20) NOT NULL DEFAULT '' COMMENT '装修情况',
`elevator` varchar(20) NOT NULL DEFAULT '' COMMENT '有无电梯',
`floor_situation` varchar(20) NOT NULL DEFAULT '' COMMENT '楼层情况',
`floor_total` int(11) NOT NULL DEFAULT 0 COMMENT '总楼层数',
`building_year` int(11) NOT NULL DEFAULT 0 COMMENT '建造年份',
`building_type` varchar(20) NOT NULL DEFAULT '' COMMENT '建造类型（板塔）',
`address` varchar(20) NOT NULL DEFAULT '' COMMENT '所在小区域',
`publish_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '房源发布时间',
`price` int(11) NOT NULL DEFAULT 0 COMMENT '房源单价',
`total_price` int(11) NOT NULL DEFAULT 0 COMMENT '房源总价',
`real_size` double NOT NULL DEFAULT 0 COMMENT '套内平米数',
`building_structure` varchar(20) NOT NULL DEFAULT '' COMMENT '建筑结构',
`fitment_situation` varchar(20) NOT NULL DEFAULT '' COMMENT '装修情况',
`stairway_rate` varchar(20) NOT NULL DEFAULT '' COMMENT '梯户比例',
`heating_way` varchar(20) NOT NULL DEFAULT '' COMMENT '供暖方式',
`property_right` int(11) NOT NULL DEFAULT 0 COMMENT '产权年限',
`link_model_price` int(11) NOT NULL DEFAULT 0 COMMENT '链家计算模型价格',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
`create_day` int(11) NOT NULL DEFAULT 0 COMMENT '创建日（yyMMdd）',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='房源表';





drop table `house_source_sale`;
CREATE TABLE `house_source_sale` (
`id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`link_house_source_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '房源id',
`publish_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '挂牌时间',
`last_transaction_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上次交易时间',
`trading_ownership` varchar(30) NOT NULL DEFAULT '' COMMENT '交易权属',
`house_usage` varchar(30) NOT NULL DEFAULT '' COMMENT '房屋用途',
`house_reburn_life` varchar(30) NOT NULL DEFAULT '' COMMENT '房屋年限',
`property_rights_belong_to` varchar(30) NOT NULL DEFAULT '' COMMENT '产权所属',
`mortgage_information` varchar(30) NOT NULL DEFAULT '' COMMENT '抵押信息',
`room_book` varchar(30) NOT NULL DEFAULT '' COMMENT '房本备件',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
`create_day` int(11) NOT NULL DEFAULT 0 COMMENT '创建日（yyMMdd）',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='房源交易扩展表';




drop table `house_source_watching`;
CREATE TABLE `house_source_watching` (
`id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`link_house_source_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '房源id',
`watching_num` int(11) NOT NULL DEFAULT 0 COMMENT '关注数',
`real_see_num` int(11) NOT NULL DEFAULT 0 COMMENT '带看数',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
`create_day` int(11) NOT NULL DEFAULT 0 COMMENT '创建日（yyMMdd）',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='房源关注表';




drop table `house_source_history_price`;
CREATE TABLE `house_source_history_price` (
`id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`link_house_source_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '房源id',
`price` int(11) NOT NULL DEFAULT 0 COMMENT '小区单价',
`total_price` int(11) NOT NULL DEFAULT 0 COMMENT '小区总价',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='房源关注表';








