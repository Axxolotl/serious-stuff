def get_personal_info(w):
    
    class_names = ['personal-wrapper', 'details-wrapper']
    nums_names = ['6', '12']
    personal_info = ''
    for i,j in zip(class_names, nums_names):
    
        personal = w.find(class_ = i).find(class_ = 'row').find_all(class_ = f'col-xs-{j} col-md-8')
        personal = [re.sub(r'[\n|\r|\t]', ' ', i.text).strip() for i in personal]

        labels = w.find(class_ = i).find(class_ = 'row').find_all(class_ = f'col-xs-{j} col-md-4 labels')
        labels = [re.sub(r'[\n|\r|\t]', '', i.text).strip() for i in labels]
    
        if i == 'personal-wrapper':
            personal_info += '<br />'.join([i + ' ' + j for i,j in zip(labels, personal)]) + '<br />___________________________________________________________________<br />'
        else:
            personal_info += '<br /><br />'.join([i + ' ' + j for i,j in zip(labels, personal)]).replace('     ', '<br /><br />')
            personal_info = personal_info.replace('  +', '<br />+')

    links = w.find(class_='details-wrapper').find(class_='col-xs-12 links').find(class_='col-xs-12 col-md-8').find_all('a')

    personal_info += '<br /><br />' + '<br />'.join([str(i) for i in links])
    return personal_info
