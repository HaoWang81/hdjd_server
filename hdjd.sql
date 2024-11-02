create table t_hdjd_blank_production
(
    id                 int auto_increment
        primary key,
    production_name    varchar(100)                          null,
    check_num          int                                   null,
    per_weight         int                                   null,
    production_company varchar(100)                          null,
    production_unit    varchar(100)                          null,
    production_date    date                                  null,
    update_time        timestamp default current_timestamp() null
);

create table t_hdjd_code_hour
(
    code int        null,
    hour varchar(5) null
);

create table t_hdjd_code_weeknum
(
    week_num  int         null,
    week_name varchar(20) null
);

create table t_hdjd_log
(
    id          int         null,
    ip          varchar(50) null,
    url         text        null,
    update_time timestamp   null
);

create table t_hdjd_lv_blank_production
(
    id                 int auto_increment
        primary key,
    production_name    varchar(100)                          null,
    check_num          int                                   null,
    per_weight         double                                null,
    production_company varchar(100)                          null,
    production_unit    varchar(100)                          null,
    custom_group       varchar(100)                          null,
    sale_country       varchar(100)                          null,
    work_group         varchar(100)                          null,
    production_date    date                                  null,
    update_time        timestamp default current_timestamp() null
);

create table t_hdjd_product_monitor
(
    id              int auto_increment
        primary key,
    changhao        varchar(100)                          null,
    zaoxingzhixin   int                                   null,
    hexiang         int                                   null,
    maopichengping  int                                   null,
    kaixiangqingli  int                                   null,
    qingli          int                                   null,
    damo            int                                   null,
    rechuli         int                                   null,
    jingxiu         int                                   null,
    caizhijianyan   int                                   null,
    maopijianyan    int                                   null,
    qinglibaozhuang int                                   null,
    tuzhuang        int                                   null,
    tuzhuangjianyan int                                   null,
    zhongjian       int                                   null,
    jiagong         int                                   null,
    jiagongqingli   int                                   null,
    jiagongjianyan  int                                   null,
    update_time     timestamp default current_timestamp() null,
    count_flag      varchar(5)                            null
);

create table t_hdjd_product_monitor_lengtie
(
    production_name    varchar(20) null,
    production_use     varchar(50) null,
    shortage_today     int         null,
    shortage_after3    int         null,
    current_week_num   int         null,
    current_month_num  int         null,
    production_company varchar(50) null
);

create table t_hdjd_product_monitor_lv
(
    id                   int auto_increment
        primary key,
    changhao             varchar(100)                          null,
    jinrizaoxing         int                                   null,
    benzhouzaoxing       int                                   null,
    benyuezaoxingqianshu int                                   null,
    jinrizhuanxu         int                                   null,
    benzhouzhuanxu       int                                   null,
    benyuezhuanxuqianshu int                                   null,
    maopichengpin        int                                   null,
    damo                 int                                   null,
    rechuli              int                                   null,
    jingxiu              int                                   null,
    maopizaizhi          int                                   null,
    jinrijiagong         int                                   null,
    benzhoujiagong       int                                   null,
    yuedujiagong         int                                   null,
    jiagongzaizhi        int                                   null,
    jinriqingli          int                                   null,
    benzhouqingli        int                                   null,
    yueduqingli          int                                   null,
    qinglizaizhi         int                                   null,
    update_time          timestamp default current_timestamp() null
);

create table t_hdjd_product_monitor_ngc
(
    id          int auto_increment
        primary key,
    changhao    varchar(100)                          null,
    zx_dmjz     int                                   null,
    zx_jrkx     int                                   null,
    zx_jrqs     int                                   null,
    zx_bzzx     int                                   null,
    zx_ydzx     int                                   null,
    dm_jrdm     int                                   null,
    dm_jrrcl    int                                   null,
    dm_jrjx     int                                   null,
    dm_jrndtjy  int                                   null,
    dm_bzdm     int                                   null,
    dm_yddm     int                                   null,
    dm_mpzz     int                                   null,
    yq_jryq     int                                   null,
    yq_jryqjy   int                                   null,
    yq_bzyq     int                                   null,
    yq_ydyq     int                                   null,
    jg_jrjg     int                                   null,
    jg_jrjgjy   int                                   null,
    jg_bzjg     int                                   null,
    jg_ydjg     int                                   null,
    jg_jgdw     varchar(50)                           null,
    jg_jgzz     int                                   null,
    mp_mpzjg    int                                   null,
    mp_bzmpzjg  int                                   null,
    mp_ydmpzjg  int                                   null,
    mp_cpk      int                                   null,
    update_time timestamp default current_timestamp() null
);

create table t_hdjd_product_monitor_tie
(
    id                    int auto_increment
        primary key,
    changhao              varchar(100)                          null,
    jinrizhixin           int                                   null,
    jinrihexiang          int                                   null,
    jinrikaixiang         int                                   null,
    benzhouhexiang        int                                   null,
    yueduzhixin           int                                   null,
    jinrizhuanxu          int                                   null,
    benzhouzhuanxu        int                                   null,
    yueduzhuanxu          int                                   null,
    yueduxiaoshou         int                                   null,
    maopichengpin         int                                   null,
    damo                  int                                   null,
    rechuli               int                                   null,
    jingxiu               int                                   null,
    maopijianyan          int                                   null,
    tuzhuang              int                                   null,
    maopizaizhi           int                                   null,
    jinrijiagong          int                                   null,
    benzhoujiagong        int                                   null,
    yuedujiagong          int                                   null,
    jiagong_yueduxiaoshou int                                   null,
    jiagongzaizhi         int                                   null,
    jinriqingli           int                                   null,
    benzhouqingli         int                                   null,
    yueduqingli           int                                   null,
    qinglizaizhi          int                                   null,
    update_time           timestamp default current_timestamp() null
);

create table t_hdjd_task
(
    id     int         null,
    userid int         null,
    date   varchar(30) null,
    task   longtext    null
);

