PGDMP                         z         
   telebot_db    14.4    14.4     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16394 
   telebot_db    DATABASE     g   CREATE DATABASE telebot_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Russian_Russia.1251';
    DROP DATABASE telebot_db;
                postgres    false            �            1259    16411    notes    TABLE     �   CREATE TABLE public.notes (
    note_id integer NOT NULL,
    user_id integer NOT NULL,
    note_text text NOT NULL,
    note_date timestamp without time zone NOT NULL
);
    DROP TABLE public.notes;
       public         heap    postgres    false            �            1259    16410    Notes_note_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Notes_note_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public."Notes_note_id_seq";
       public          postgres    false    210            �           0    0    Notes_note_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public."Notes_note_id_seq" OWNED BY public.notes.note_id;
          public          postgres    false    209            \           2604    16414    notes note_id    DEFAULT     p   ALTER TABLE ONLY public.notes ALTER COLUMN note_id SET DEFAULT nextval('public."Notes_note_id_seq"'::regclass);
 <   ALTER TABLE public.notes ALTER COLUMN note_id DROP DEFAULT;
       public          postgres    false    209    210    210            �          0    16411    notes 
   TABLE DATA           G   COPY public.notes (note_id, user_id, note_text, note_date) FROM stdin;
    public          postgres    false    210   �
       �           0    0    Notes_note_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public."Notes_note_id_seq"', 98, true);
          public          postgres    false    209            ^           2606    16418    notes Notes_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.notes
    ADD CONSTRAINT "Notes_pkey" PRIMARY KEY (note_id);
 <   ALTER TABLE ONLY public.notes DROP CONSTRAINT "Notes_pkey";
       public            postgres    false    210            �   ~
  x��ZKoU����,H��~?NUe��J頙DbP�/���ߔ2��H�J�����Nnc��������~k�s�s�u1���l�=w��Z�zܽP�u�K�;��qʝ�R�y�,���Ǖ �F�:�7o��R�J��;#MJ�3J�3����]2+�+�KA�2�Ȉ�����q��ָ7:�)��o"U�s��/|��#sU!e�J/�V(ۡ�tq���Kr#+�Jm�F��G���z�~��*��E�SO��f��/��z���?+�~�[��E��ު_Փ�AQ_�j�Ӣ*�*J�J��Z�*��!a�
]��˲,��N=y�����W�-�@�Z�J���Y�1�ǥR� ��Q�8�0*�_Vk+�K�����z��'R�*'�\�^�ԡ�p���!���*���$��f:�t���2I�B�������Ǣ+�!� T�w�6�b-	�k���fh�tCzUISڨBRBw�T�|Y�4�eQ?nn�Q��
\�Y4_0&!���C��r��E,7�x�Y��@�Ϥ��Y�%a���o7� ÌA�>����l��`�A��^�d�@B�|�q�}�ͭd�-3ϵ<�#��`��	e�j��f�+�l���z�Y���	�k_��|��31y#t7��S��j�7F�"�x1!��Y'Ȉ=���ɕ�
Ζ=����������̇�\�7�mN�Ro�M��O[KJ@<�P��mBEfw��:{B���xBj�d=�����F��� �=�N�%4��UJ.*P;p����L%-'�� v������@ ��!cO0wB���*CL�[�cGѡ����D)�Л��ez�Jt%�0rV�1,���HCi�馹��>��T=���za����O�ߜ+>�P���lt��՛����b�~_}6*�?_��W/ˣŏFC�-A��d� �z�P�l@-7v�~X��*e�d�%�ts@�4�u�2�e�5��7�ڊ�],���%aB�Vi5J|i��6����Δ&��p�n�O��i�Nʨ��)�<K̲�T:-���  ��^�ܖ>��A�O�H=Aj��&���j��V�(�=�%��<��u'x�q�� ���gd���R�����׮-����%�椰2���B9�N�nX���AN�����?�z��e�h��Z��畟�B�W���T��������~ct�3�0�etNF�ۛ~U�pox���)Yj�1r�	~VI=:�w\[���S]�=�Y�[�������߼�m�������4�|����_��:�^��j��X5;�
λ�l���e>����m�v���������y�ݦ���Ä�s�n�uG����5�P�
�ʣ�t�]%y${�YǋWd2Fv�}��l>�Evo6aek�v;�L_�6j�ϲ�Yo6���F��p�Zn���	:�}��4�W����ca��J �;S��!��9���WU��v�	@���.��U��msZ'#8�����fm�a�i�`=?">�m������	��ͩ�<��=���ϙ�y�X�c�l'�@<��t�0�f������1��{o�. ��7Ghn��f:��{�����My9L<T��y���0�ppy3^�ݪ��Lyl�:u�T�(�w�"�k�d����e0�͙^bf��dc��P�c\�
�1��`�Ӑ���p���I��?Y��l�3��)w�r�)�s�\8M�Ӕ;M��#�
VY�b7���-R�[6��#1U���y|�ct�$� ��k��s=e�<����_p�Kj��1�t=���T�(֖>Z�����I�"o��p���׹O�"������w�g���X)|�ʤ$��x�U�%�H1����]���fcnV�Q��NY/|�����.j���~�)ɮ��`DM��-��e��qطu�{{���}֗)�@��V�Zk �S���t(m��Z�{]�e�R�ܹ����e��I����I��Ȃ��[m��?��^�,/\,�P,}V\,~Y,�\ ���Tp§~`W��|Zr�#p�A�v��}y��u�+YIZ�����g��˫���9Æ�[/����}֋F�hyuk˨�A%�ꭙ�^�[��ޖ��i��FRj�:����������=�	�������>=�ok��=;DY�P&��7"�~Ai���+rfn�ٿ;�J�wm}�����I�Ϛ;9���/~a��ү��ދ����G+��~Εaj�VN׎���e`�y�^W�� ]�[��������ԑ�ou
��E�����p�Ł��K��l���AͻmKcULV�����i>3���W�N�m���ޑ�P�����rx5�S�d�v"t�{�xRx�+�Y6�1Az�i	��<}Q]����ߞ�D+/�����I�^�>:t���	�I]�LQ�V�K�<V�U�R"v�1u/�3��U�R��z�o�u��.��IG�I��:��^�^���4��2�ׯ��� J����I�Mw���э���xiܹT��R�5~��-��Q\q�5&��Y.G5&�ԉ魸h�O���6Q$��\�Q��I$��L��)�#u��h�\,,�X��t~�X�6����e��"�h����R7�_�t4PHz�E�k�HvȐ���z,'-Xq�00%w"�3S��Ĕ�#ƌ�e��F�TI"N�+�,=C�<$�O.:h:�\�)��_y��|�F�+��Q*a     