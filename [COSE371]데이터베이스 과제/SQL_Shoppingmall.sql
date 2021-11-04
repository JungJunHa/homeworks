drop table delivery;
drop table orders;
drop table product;
drop table users;
drop table addressbook;

create table addressbook(address varchar(50), zipcode varchar(20), primary key (address));
create table users(id varchar(20), password varchar(20), name varchar(20), phone varchar(11), address varchar(50), card_info varchar(50), primary key (id), foreign key (address) references addressbook);
create table product(product_id varchar(20), name varchar(20), amount integer, price numeric(8,2), detail varchar(100), primary key (product_id));
create table orders(product_id varchar(20), user_id varchar(20), product_number integer, product_price numeric(8,2), sum_price numeric(8,2), primary key (product_id, user_id), foreign key (product_id) references product, foreign key (user_id) references users(id));
create table delivery(user_id varchar(20), sum_price numeric(8,2), date varchar(30), primary key (user_id));

insert into addressbook values ('seoul','11111');
insert into addressbook values ('gurogu','22222');
insert into addressbook values ('gangnam','33333');
insert into addressbook values ('gangdong','44444');
insert into addressbook values ('gangbuk','55555');
insert into addressbook values ('gangseo','66666');

insert into users values ('11111','01234','Jung','01011111111','seoul','삼성카드');
insert into users values ('22222','01231','Min','01022222222','gangbuk','신한카드');
insert into users values ('33333','01235','Kim','01033333333','gangseo','신한카드');
insert into users values ('44444','01233','Jay','01044444444','gangdong','국민카드');
insert into users values ('55555','01237','Bam','01055555555','gangnam','국민카드');
insert into users values ('66666','01239','Jeon','01066666666','gurogu','신한카드');
insert into users values ('77777','01238','Park','01077777777','seoul','삼성카드');

insert into product values ('11111','디퓨저',50,5000, '미니 디퓨저로, 차량이나 사무실 등 다양한 곳에 놓을 수 있는 제품입니다.');
insert into product values ('22222','라이언인형',40,4000,'여자친구에게 선물하기 딱 좋은, 그런 인형입니다.');
insert into product values('33333','무드등', 60,6000,'사무실이나 어두운 방을 밝게! 자취생들을 위한 아이템 무드등입니다.');
insert into product values('44444','수면양말',70,3000,'요즘 잠 안오는 분들을 위한 필수 아이템! 신고만 있 어도 잠이 솔솔');