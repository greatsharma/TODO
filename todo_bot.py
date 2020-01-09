import os
import re
import json


def update_dispatcher(conn, db, update):
    try:
        chat_id = update['message']['chat']['id']
        msg = update['message']['text']
        
        if re.match('/[sS]tart', msg):
            conn.send_message(chat_id, 'hey,  I am to-Do  ^-^\n\n click /help to know me more :)')

        elif re.match('/[hH]elp', msg):
            conn.send_message(chat_id, 'To create new list type:\n c/Create <list name> <item1 item2 ...>.\n\n'+\
                                        'To add item type:\n a/Add <list name> <item1 item2 ...>.\n\n' + \
                                        'To remove item from list(GUI) type:\n r/Remove from <list name>.\n\n' + \
                                        'To remove item from list manually type:\n r/Remove <item1 item2 ...> from <list name>.\n\n' + \
                                        'To view list type:\n v/View <list name>.\n\n' + \
                                        'To delete list type:\n c/Clear <list name>.\n\n' + \
                                        'To view all lists name type:\n s/Show lists.')

        elif re.match('[cC]reate .+ .+', msg):
            _create_list(conn, db, chat_id, msg)
            
        elif re.match('[aA]dd .+ .+', msg):
            _add_item_to_list(conn, db, chat_id, msg)

        elif re.match('[rR]emove from .+', msg):
            _remove_item_keyboard_view(conn, db, chat_id, msg)
                
        elif re.match('[rR]emove .+ from .+', msg):
            _remove_item_from_list(conn, db, chat_id, msg)
            
        elif re.match('[cC]lear .+', msg):
            _clear_list(conn, db, chat_id, msg)
            
        elif re.match('[vV]iew .+', msg):
            _view_list(conn, db, chat_id, msg)
            
        elif re.match('[sS]how lists*', msg):
            _show_lists_name(conn, db, chat_id)
            
        else:
            conn.send_message(chat_id, 'Unable to understand :(\n\n type /help to know me more :)')

    except Exception as e:
        print('\nerror while handling update, error descr -> \n{}'.format(e))
        conn.send_message(chat_id, 'oops... something went wrong :( \n\ntry again...')


def _create_list(conn, db, chat_id, msg):
    item = msg.split()
    list_name = item[1]

    del item[0:2]

    rows = db.search_item('items', 'owner_id = "{}" AND list_name = "{}"'.format(chat_id, list_name), return_list=True)

    if not len(rows):
        for item_name in item:
            if not db.add_item('items', {'owner_id':chat_id, 'list_name': list_name, 'item_name': item_name}):
                conn.send_message(chat_id, "unable to add {} to {} :( \n\ntry again...)".format(item_name, list_name))
            else:
                conn.send_message(chat_id, '{} added to {} list'.format(item_name, list_name))
    else:
        conn.send_message(chat_id, 'list {} already present. \n\n type show lists, for all active lists.'.format(list_name))


def _add_item_to_list(conn, db, chat_id, msg):
    item = msg.split()
    list_name = item[1]
    del item[0:2]

    rows = db.search_item('items', 'owner_id = "{}" AND list_name = "{}"'.format(chat_id, list_name), return_list=True)

    old_items = []
    for row in rows:
        old_items.append(row[2])

    if not len(rows):
        for item_name in item:
            
            if item_name in old_items:
                conn.send_message(chat_id, '{} already present in {}.'.format(item_name, list_name))
                old_items.remove(item_name)
            else:
                if not db.add_item('items', {'owner_id':chat_id, 'list_name': list_name, 'item_name': item_name}):
                    conn.send_message(chat_id, "unable to add this item to the list :( \n\ntry again...")
                else:
                    conn.send_message(chat_id, '{} added to {} list'.format(item_name, list_name))
    else:
        conn.send_message(chat_id, 'No list named {}. \n\n'.format(list_name) + \
                                    'to create new list type:\n c/Create <list name> <item1 item2 ...> :)')


def _remove_item_keyboard_view(conn, db, chat_id, msg):
    list_name = msg.split()[2]
    item_list = db.fetch_items('items', 'item_name', 'owner_id = "{}" AND list_name = "{}"'.format(chat_id, list_name))

    items = []
    for item in item_list:
        items.append(item[0])

    if items:
        keyboard = list(map(lambda x: ['remove ' + x + ' from ' + list_name], items))
        reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True}

        conn.send_message(chat_id, 'select an item to delete', json.dumps(reply_markup))
        

def _remove_item_from_list(conn, db,chat_id, msg):
    item = msg.split()
    list_name = item[len(item)-1]
    del item[0]
    del item[-2:]
    
    if db.search_item('items', 'owner_id = "{}" AND list_name = "{}"'.format(chat_id, list_name)):
        for item_name in item:
            status , descr = db.delete_item('items', 'owner_id = "{}" AND list_name = "{}" AND item_name = "{}"'.format(chat_id, list_name, item_name))

            if not status:
                conn.send_message(chat_id, descr)
            else:
                conn.send_message(chat_id, '{} removed from list {}.'.format(item_name, list_name))
    else:
        conn.send_message(chat_id, 'No list named {}. \n\ntry again...'.format(list_name))
    

def _clear_list(conn, db, chat_id, msg):
    list_name = msg.split()[1]

    if not db.delete_item('items', 'owner_id = "{}" AND list_name = "{}"'.format(chat_id, list_name)):
        conn.send_message(chat_id, 'unable to clear to-do list :( \n\ntry again...')
    else:
        conn.send_message(chat_id, 'list {} deleted :)'.format(list_name))


def _view_list(conn, db, chat_id, msg):
    list_name = msg.split()[1]
    item_list = db.fetch_items('items', 'item_name', 'owner_id = "{}" AND list_name = "{}"'.format(chat_id, list_name))

    items = []
    for item in item_list:
        items.append(item[0])

    if items:
        conn.send_message(chat_id, '\n'.join(items))
    else:
        conn.send_message(chat_id, 'No list named {}.\n\n type <show lists>, for all active lists.'.format(list_name))


def _show_lists_name(conn, db, chat_id):
    all_lists = db.advance_search('SELECT DISTINCT list_name FROM items WHERE owner_id = "{}"'.format(chat_id))
                
    lists_name = []
    for l_name in all_lists:
        lists_name.append(l_name[0])

    if lists_name:
        keyboard = list(map(lambda x: ['view ' + x ], lists_name))
        reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True}

        conn.send_message(chat_id, 'select list to view items', json.dumps(reply_markup))
    else:
        conn.send_message(chat_id, 'no list is active. \n\n' + \
                                   'to create new list type:\n c/Create followed by list name followed by items with spaces :)')
