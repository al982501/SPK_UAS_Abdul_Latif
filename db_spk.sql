PGDMP         ;                {            db_spk    15.4    15.4     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16397    db_spk    DATABASE     }   CREATE DATABASE db_spk WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Indonesia.1252';
    DROP DATABASE db_spk;
                postgres    false            �            1259    16399    tb_mobil    TABLE     H  CREATE TABLE public.tb_mobil (
    no integer NOT NULL,
    nama_mobil character varying(255) NOT NULL,
    harga character varying(255) NOT NULL,
    warna character varying(255) NOT NULL,
    merk character varying(255) NOT NULL,
    tahun_rilis character varying(255) NOT NULL,
    garansi character varying(255) NOT NULL
);
    DROP TABLE public.tb_mobil;
       public         heap    postgres    false            �            1259    16398    tb_mobil_no_seq    SEQUENCE     �   CREATE SEQUENCE public.tb_mobil_no_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.tb_mobil_no_seq;
       public          postgres    false    215            �           0    0    tb_mobil_no_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.tb_mobil_no_seq OWNED BY public.tb_mobil.no;
          public          postgres    false    214            e           2604    16402    tb_mobil no    DEFAULT     j   ALTER TABLE ONLY public.tb_mobil ALTER COLUMN no SET DEFAULT nextval('public.tb_mobil_no_seq'::regclass);
 :   ALTER TABLE public.tb_mobil ALTER COLUMN no DROP DEFAULT;
       public          postgres    false    214    215    215            �          0    16399    tb_mobil 
   TABLE DATA           \   COPY public.tb_mobil (no, nama_mobil, harga, warna, merk, tahun_rilis, garansi) FROM stdin;
    public          postgres    false    215   j       �           0    0    tb_mobil_no_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.tb_mobil_no_seq', 10, true);
          public          postgres    false    214            g           2606    16406    tb_mobil tb_mobil_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.tb_mobil
    ADD CONSTRAINT tb_mobil_pkey PRIMARY KEY (no);
 @   ALTER TABLE ONLY public.tb_mobil DROP CONSTRAINT tb_mobil_pkey;
       public            postgres    false    215            �   8  x�U��r�0��7O�e�h'	Dd@���	�j��8:%��t",��E����9'߹���8P���<���N{`�`�A&��$-R,�Eш��0#��j�u��o����A���@%^��uU�/�Ճ�r���M��^�!��q��cw�R�� �*2�prGט_ӫI�"�Ň �pzt�16�� ^H!S\�>�Kf�� ��Ze�T�#Dݔ΅l��׉ 6v�s��C��Q�߉��9D"MDS�߰,������۪�ҝ�NG�ȇ0m�p<��Gb�3�3���]���|j�����o5�J�|F�c�s�     