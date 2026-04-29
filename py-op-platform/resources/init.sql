/*****************************************************
 * @software: PyCharm
 * @author: Beau Dean
 * @contact: https://fairy.host
 * @organization: https://github.com/FairylandFuture
 * @datetime: 2026-04-29 19:05:45 UTC+08:00
 *****************************************************/

create database if not exists py_op_platform default charset utf8mb4 collate utf8mb4_general_ci;
use py_op_platform;
create table app_host_machine
(
    id         bigint primary key auto_increment comment '主机id',
    hostname   varchar(63)     not null comment '主机名称',
    password   varchar(255)    not null comment '主机密码',
    ipv4       int             not null comment '主机ipv4地址',
    online     enum ('Y', 'N') not null comment '是否在线',
    created_at datetime        not null default current_timestamp comment '创建时间',
    updated_at datetime        not null default current_timestamp on update current_timestamp comment '更新时间',
    enabled    enum ('Y', 'N') not null default 'Y' comment '逻辑状态'
) comment '主机表';

create table app_host_room
(
    id         bigint primary key auto_increment comment '机房id',
    name       varchar(63)     not null comment '机房名称',
    created_at datetime        not null default current_timestamp comment '创建时间',
    updated_at datetime        not null default current_timestamp on update current_timestamp comment '更新时间',
    enabled    enum ('Y', 'N') not null default 'Y' comment '逻辑状态'
) comment '机房表';

create table app_host_room_machine
(
    id         bigint primary key auto_increment comment 'id',
    room_id    bigint          not null comment '机房id',
    machine_id bigint          not null comment '机房id',
    created_at datetime        not null default current_timestamp comment '创建时间',
    updated_at datetime        not null default current_timestamp on update current_timestamp comment '更新时间',
    enabled    enum ('Y', 'N') not null default 'Y' comment '逻辑状态'
) comment '机房和主机关联表';

create table app_host_region
(
    id         bigint primary key auto_increment comment '区域id',
    name       varchar(31)     not null comment '区域名称',
    created_at datetime        not null default current_timestamp comment '创建时间',
    updated_at datetime        not null default current_timestamp on update current_timestamp comment '更新时间',
    enabled    enum ('Y', 'N') not null default 'Y' comment '逻辑状态'
) comment '区域表';

create table app_host_region_room
(
    id         bigint primary key auto_increment comment 'id',
    region_id  bigint          not null comment '区域id',
    room_id    bigint          not null comment '机房id',
    created_at datetime        not null default current_timestamp comment '创建时间',
    updated_at datetime        not null default current_timestamp on update current_timestamp comment '更新时间',
    enabled    enum ('Y', 'N') not null default 'Y' comment '逻辑状态'
) comment '区域和机房关联表';

create table app_host_region_statistic_host
(
    id         bigint primary key auto_increment comment 'id',
    region_id  bigint          not null comment '区域id',
    total      int             not null default 0 comment '统计的数量',
    created_at datetime        not null default current_timestamp comment '创建时间',
    updated_at datetime        not null default current_timestamp on update current_timestamp comment '更新时间',
    enabled    enum ('Y', 'N') not null default 'Y' comment '逻辑状态'
) comment '区域维度统计主机总数';

create table app_host_room_statistic_host
(
    id         bigint primary key auto_increment comment 'id',
    room_id    bigint          not null comment '机房id',
    total      int             not null default 0 comment '统计的数量',
    created_at datetime        not null default current_timestamp comment '创建时间',
    updated_at datetime        not null default current_timestamp on update current_timestamp comment '更新时间',
    enabled    enum ('Y', 'N') not null default 'Y' comment '逻辑状态'
) comment '机房维度统计主机总数'
