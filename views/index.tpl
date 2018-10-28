% rebase('base.tpl', title=title, itson=itson)
<div class="row">&nbsp;</div>
<div class="back index text-center">
%if itson:
    <div class="alert alert-success">It's ON!</div>
    % for r in sessions:
        <div>
        % if r['ended']:
            I surfed {{ r['duration'] }}
            <a href="#" >@{{ r['spot'] }}</a>.
        % else:
            I'm surfing
            <a href="#" >@{{ r['spot'] }}</a>
            since {{ r['duration'] }}.
        % end
        </div>
    %end
    </div>
%else:
    <div class="alert alert-light">No surf today...</div>
%end
</div>
