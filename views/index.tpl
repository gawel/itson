% rebase('base.tpl', title=title, itson=itson)
<div class="back index text-center">
%if itson:
    <div class="alert alert-success">{{ title }}</div>
    % for r in sessions:
        <div>
        % if r['ended']:
            I surfed {{ r['size'] }} waves during {{ r['duration'] }}
            <a target="new" href="{{ r['report_url'] }}">@{{ r['spot'] }}</a>.
        % else:
            I'm surfing
            <a target="new" href="{{ r['report_url'] }}">@{{ r['spot'] }}</a>
            since {{ r['duration'] }}.
        % end
        </div>
    %end
    </div>
%else:
    <div class="off">{{ title }}</div>
%end
</div>
